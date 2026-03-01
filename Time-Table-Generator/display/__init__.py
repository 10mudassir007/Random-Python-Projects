"""
Pretty-printing utilities for timetables.

Only batch-wise timetables — each batch shows its weekly grid with
subject names, followed by a Subject : Teacher Name mapping.
"""

from database import DAYS, SLOTS, SUBJECTS_DB, DEPARTMENTS_DB, BREAK_AFTER, BREAK_LABEL


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _separator(char: str = "-", width: int = 120) -> str:
    return char * width


def _active_slots_for_day(schedule: dict, day: str) -> int:
    """Return the number of contiguous filled slots from the top on *day*."""
    count = 0
    for slot in SLOTS:
        if schedule[day][slot] is not None:
            count += 1
        else:
            break
    return count


# ─────────────────────────────────────────────────────────────────────────────
# Batch timetable
# ─────────────────────────────────────────────────────────────────────────────

def format_batch_timetable(dept_name: str, batch: str, schedule: dict) -> str:
    """
    Return a formatted string for one batch's weekly timetable.

    - Shows subject names in the grid (not codes).
    - Only shows active (filled) rows — no trailing empty rows.
    - Ends with a  Subject : Teacher Name  mapping.
    """
    col_w = 24
    header_w = 14
    lines: list[str] = []

    lines.append(_separator("="))
    lines.append(f"  Department : {dept_name}")
    lines.append(f"  Batch      : {batch}")

    # Per-day class counts
    day_counts = {day: _active_slots_for_day(schedule, day) for day in DAYS}
    total = sum(day_counts.values())
    counts_str = "  Classes/day: " + " | ".join(
        f"{d[:3]} {day_counts[d]}" for d in DAYS
    ) + f"  (Total: {total}/week)"
    lines.append(counts_str)
    lines.append(_separator("="))

    # Column header
    header = f"{'Slot':<{header_w}}" + "".join(f"{d:^{col_w}}" for d in DAYS)
    lines.append(header)
    lines.append(_separator())

    max_rows = max(day_counts.values()) if day_counts else 0

    for si in range(max_rows):
        slot = SLOTS[si]
        row = f"{slot:<{header_w}}"
        for day in DAYS:
            entry = schedule[day][slot]
            if entry:
                # Show subject name (truncated to fit column)
                cell = entry["subject"][:col_w - 2]
            else:
                cell = ""
            row += f"{cell:^{col_w}}"
        lines.append(row)

        # Insert a visual break row after the break-boundary slot
        if si == BREAK_AFTER and si < max_rows - 1:
            brk = f"{BREAK_LABEL:<{header_w}}" + f"{'*** BREAK ***':^{col_w * len(DAYS)}}"
            lines.append(brk)

    # ── Subject : Teacher Name mapping ───────────────────────────────────────
    lines.append("")
    lines.append(f"  {'Subject':<40} {'Teacher'}")
    lines.append("  " + "─" * 70)

    seen: set[str] = set()
    for day in DAYS:
        for slot in SLOTS:
            entry = schedule[day][slot]
            if entry and entry["subject_code"] not in seen:
                seen.add(entry["subject_code"])
                subj_label = f"{entry['subject_code']} — {entry['subject']}"
                lines.append(f"  {subj_label:<40} {entry['teacher']}")

    lines.append("")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────

def format_summary(timetable: dict) -> str:
    """Return a summary of total scheduled classes per batch."""
    lines: list[str] = []
    lines.append(_separator("="))
    lines.append("  TIMETABLE SUMMARY")
    lines.append(_separator("="))

    for dept_code, dept in timetable.items():
        dept_name = DEPARTMENTS_DB[dept_code]["name"]
        lines.append(f"\n  [{dept_code}] {dept_name}")
        for batch, schedule in dept.items():
            day_totals = []
            for day in DAYS:
                count = sum(1 for slot in SLOTS if schedule[day][slot])
                day_totals.append(count)
            total = sum(day_totals)
            breakdown = ", ".join(
                f"{DAYS[i][:3]}={day_totals[i]}" for i in range(len(DAYS))
            )
            lines.append(
                f"    {batch}: {total} hrs/week  ({breakdown})"
            )
    lines.append("")
    return "\n".join(lines)
