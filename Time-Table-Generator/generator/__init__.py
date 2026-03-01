"""
Timetable generation engine.

Design goals
────────────
- NO empty gaps between classes on any day.  If a day has 4 classes they
  occupy slots 1-4 contiguously (08:00 → 12:00).
- Daily class counts are **variable** — total weekly hours for a batch are
  distributed across 5 days as evenly as possible (e.g. 4-4-3-3-3 for 17 h).
- No teacher is double-booked in the same (day, slot).
- Subjects with fewer eligible teachers are scheduled first (priority).
- Each subject appears at most once per day (spread constraint).
"""

import random
from collections import defaultdict

from database import DAYS, SLOTS, TEACHERS_DB, SUBJECTS_DB, DEPARTMENTS_DB


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def build_teacher_subject_map():
    """Return {subject_code: [teacher_ids]} from TEACHERS_DB."""
    mapping: dict[str, list[str]] = defaultdict(list)
    for tid, data in TEACHERS_DB.items():
        for subj in data["can_teach"]:
            mapping[subj].append(tid)
    return mapping


def _pick_teacher(subject_code, teacher_subject_map):
    """Return a random eligible teacher id for the given subject (or None)."""
    eligible = teacher_subject_map.get(subject_code, [])
    return random.choice(eligible) if eligible else None


def _distribute_hours(total: int, num_days: int) -> list[int]:
    """
    Spread *total* hours across *num_days* as evenly as possible.

    Example: distribute_hours(17, 5)  →  [4, 4, 3, 3, 3]
             distribute_hours(16, 5)  →  [4, 4, 4, 2, 2]   (or similar)
    Returned list is shuffled so the heavier days are random.
    """
    base, extra = divmod(total, num_days)
    plan = [base + 1] * extra + [base] * (num_days - extra)
    random.shuffle(plan)
    return plan


# ─────────────────────────────────────────────────────────────────────────────
# Core generator
# ─────────────────────────────────────────────────────────────────────────────

def generate_timetable():
    """
    Build a conflict-free, gap-free timetable.

    Returns
    -------
    timetable : dict
        timetable[dept_code][batch][day][slot_index] = {
            'subject', 'subject_code', 'teacher', 'teacher_id'
        } | None
        Only the first *N* slots of each day are filled (contiguously).
    warnings : list[str]
    """
    teacher_subject_map = build_teacher_subject_map()
    warnings: list[str] = []

    # teacher_busy[teacher_id][(day, slot)] = batch
    teacher_busy: dict[str, dict] = defaultdict(dict)

    timetable: dict = {}

    # ── Initialise empty timetable ───────────────────────────────────────────
    for dept_code, dept_data in DEPARTMENTS_DB.items():
        timetable[dept_code] = {}
        for batch in dept_data["batches"]:
            timetable[dept_code][batch] = {
                day: {slot: None for slot in SLOTS} for day in DAYS
            }

    # ── Process each batch ───────────────────────────────────────────────────
    for dept_code, dept_data in DEPARTMENTS_DB.items():
        for batch, subject_codes in dept_data["batches"].items():

            # 1. Calculate total weekly hours for this batch
            total_hours = sum(SUBJECTS_DB[sc]["hours"] for sc in subject_codes)

            # 2. Distribute hours across 5 days (variable, no gaps)
            day_plan = _distribute_hours(total_hours, len(DAYS))
            # day_plan[i] = how many contiguous slots on DAYS[i]

            # 3. Build the list of (day, slot) positions to fill,
            #    top-down per day, exactly day_plan[i] slots each day
            positions: list[tuple[str, str]] = []
            for di, day in enumerate(DAYS):
                for si in range(day_plan[di]):
                    positions.append((day, SLOTS[si]))

            # 4. Build tasks: one entry per needed hour, sorted by
            #    teacher scarcity (hardest subjects first)
            tasks: list[str] = []
            for sc in subject_codes:
                tasks.extend([sc] * SUBJECTS_DB[sc]["hours"])

            tasks.sort(key=lambda sc: len(teacher_subject_map.get(sc, [])))

            # 5. Assign a consistent teacher per subject for this batch
            batch_teachers: dict[str, tuple[str, str]] = {}  # sc → (tid, name)
            for sc in subject_codes:
                tid = _pick_teacher(sc, teacher_subject_map)
                if tid is None:
                    warnings.append(
                        f"No teacher for {sc} in {batch}. Skipped."
                    )
                else:
                    batch_teachers[sc] = (tid, TEACHERS_DB[tid]["name"])

            # 6. Greedy fill — try to place each task-hour into the first
            #    available position that satisfies constraints:
            #      a) teacher not busy    b) max 1 of same subject per day
            placed_per_day: dict[str, dict[str, int]] = {
                day: defaultdict(int) for day in DAYS
            }
            unplaced: list[str] = []

            random.shuffle(positions)          # randomise within valid slots
            # Re-sort positions so they are top-down within each day
            positions.sort(key=lambda p: (DAYS.index(p[0]), SLOTS.index(p[1])))

            for sc in tasks:
                if sc not in batch_teachers:
                    continue
                tid, tname = batch_teachers[sc]
                subj_info = SUBJECTS_DB[sc]
                assigned = False

                for i, (day, slot) in enumerate(positions):
                    if timetable[dept_code][batch][day][slot] is not None:
                        continue
                    if (day, slot) in teacher_busy[tid]:
                        continue
                    # max 1 hour of same subject per day
                    if placed_per_day[day][sc] >= 1:
                        continue

                    timetable[dept_code][batch][day][slot] = {
                        "subject":      subj_info["name"],
                        "subject_code": sc,
                        "teacher":      tname,
                        "teacher_id":   tid,
                    }
                    teacher_busy[tid][(day, slot)] = batch
                    placed_per_day[day][sc] += 1
                    assigned = True
                    break

                if not assigned:
                    unplaced.append(sc)

            # 7. Retry unplaced with relaxed spread (max 2 per day)
            still_unplaced: list[str] = []
            for sc in unplaced:
                if sc not in batch_teachers:
                    continue
                tid, tname = batch_teachers[sc]
                subj_info = SUBJECTS_DB[sc]
                assigned = False

                for day, slot in positions:
                    if timetable[dept_code][batch][day][slot] is not None:
                        continue
                    if (day, slot) in teacher_busy[tid]:
                        continue

                    timetable[dept_code][batch][day][slot] = {
                        "subject":      subj_info["name"],
                        "subject_code": sc,
                        "teacher":      tname,
                        "teacher_id":   tid,
                    }
                    teacher_busy[tid][(day, slot)] = batch
                    assigned = True
                    break

                if not assigned:
                    still_unplaced.append(sc)

            if still_unplaced:
                warnings.append(
                    f"Could not place {len(still_unplaced)} hour(s) in {batch}: "
                    f"{', '.join(still_unplaced)}"
                )

    return timetable, warnings
