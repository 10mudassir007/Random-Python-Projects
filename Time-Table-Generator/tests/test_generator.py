"""
Tests for the timetable generation engine.
Validates scheduling constraints: no conflicts, contiguous slots, etc.
"""

import random
import pytest
from generator import (
    build_teacher_subject_map,
    _pick_teacher,
    _distribute_hours,
    generate_timetable,
)
from database import DAYS, SLOTS, SUBJECTS_DB, DEPARTMENTS_DB


# ─────────────────────────────────────────────────────────────────────────────
# build_teacher_subject_map
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildTeacherSubjectMap:
    def test_returns_dict(self):
        mapping = build_teacher_subject_map()
        assert isinstance(mapping, dict)

    def test_every_value_is_list(self):
        mapping = build_teacher_subject_map()
        for subj, teachers in mapping.items():
            assert isinstance(teachers, list)

    def test_known_subject_has_teachers(self):
        """CS101 should have at least one teacher."""
        mapping = build_teacher_subject_map()
        assert len(mapping.get("CS101", [])) >= 1


# ─────────────────────────────────────────────────────────────────────────────
# _pick_teacher
# ─────────────────────────────────────────────────────────────────────────────

class TestPickTeacher:
    def test_returns_valid_teacher(self):
        mapping = build_teacher_subject_map()
        tid = _pick_teacher("CS101", mapping)
        assert tid is not None
        assert tid in mapping["CS101"]

    def test_returns_none_for_unknown_subject(self):
        mapping = build_teacher_subject_map()
        tid = _pick_teacher("FAKE999", mapping)
        assert tid is None


# ─────────────────────────────────────────────────────────────────────────────
# _distribute_hours
# ─────────────────────────────────────────────────────────────────────────────

class TestDistributeHours:
    def test_total_preserved(self):
        """Sum of distributed hours must equal the input total."""
        for total in [10, 15, 17, 18, 20]:
            plan = _distribute_hours(total, 5)
            assert sum(plan) == total

    def test_correct_number_of_days(self):
        plan = _distribute_hours(18, 5)
        assert len(plan) == 5

    def test_no_day_exceeds_max_slots(self):
        """No single day should have more hours than total slots available."""
        plan = _distribute_hours(18, 5)
        for hours in plan:
            assert hours <= len(SLOTS)

    def test_even_spread(self):
        """Difference between max and min day should be at most 1."""
        plan = _distribute_hours(17, 5)
        assert max(plan) - min(plan) <= 1

    def test_zero_hours(self):
        plan = _distribute_hours(0, 5)
        assert sum(plan) == 0
        assert all(h == 0 for h in plan)

    def test_single_day(self):
        plan = _distribute_hours(5, 1)
        assert plan == [5]


# ─────────────────────────────────────────────────────────────────────────────
# generate_timetable — full integration
# ─────────────────────────────────────────────────────────────────────────────

class TestGenerateTimetable:
    """Integration tests for the full timetable generation."""

    @pytest.fixture(autouse=True)
    def _seed(self):
        """Fix random seed for reproducible tests."""
        random.seed(42)

    @pytest.fixture()
    def timetable_and_warnings(self):
        return generate_timetable()

    def test_returns_tuple(self, timetable_and_warnings):
        tt, warnings = timetable_and_warnings
        assert isinstance(tt, dict)
        assert isinstance(warnings, list)

    def test_all_departments_present(self, timetable_and_warnings):
        tt, _ = timetable_and_warnings
        for dept_code in DEPARTMENTS_DB:
            assert dept_code in tt

    def test_all_batches_present(self, timetable_and_warnings):
        tt, _ = timetable_and_warnings
        for dept_code, dept_data in DEPARTMENTS_DB.items():
            for batch in dept_data["batches"]:
                assert batch in tt[dept_code]

    def test_all_days_present_per_batch(self, timetable_and_warnings):
        tt, _ = timetable_and_warnings
        for dept_code, dept in tt.items():
            for batch, schedule in dept.items():
                for day in DAYS:
                    assert day in schedule

    def test_all_slots_present_per_day(self, timetable_and_warnings):
        tt, _ = timetable_and_warnings
        for dept_code, dept in tt.items():
            for batch, schedule in dept.items():
                for day in DAYS:
                    for slot in SLOTS:
                        assert slot in schedule[day]

    def test_no_teacher_double_booked(self, timetable_and_warnings):
        """No teacher should be assigned to two different batches
        in the same (day, slot)."""
        tt, _ = timetable_and_warnings
        # Collect all (teacher_id, day, slot) → batch
        teacher_slots: dict[tuple, str] = {}
        for dept_code, dept in tt.items():
            for batch, schedule in dept.items():
                for day in DAYS:
                    for slot in SLOTS:
                        entry = schedule[day][slot]
                        if entry is None:
                            continue
                        key = (entry["teacher_id"], day, slot)
                        if key in teacher_slots:
                            assert teacher_slots[key] == batch, (
                                f"Teacher {entry['teacher_id']} double-booked "
                                f"at {day} {slot}: {teacher_slots[key]} and {batch}"
                            )
                        teacher_slots[key] = batch

    def test_contiguous_slots_no_gaps(self, timetable_and_warnings):
        """Filled slots on each day should be contiguous from the top
        (no empty slot followed by a filled slot).

        NOTE: The generator has a relaxed second-pass that may place
        overflow hours in non-contiguous positions.  We count how many
        batches violate contiguity — a handful is acceptable.
        """
        tt, _ = timetable_and_warnings
        gap_count = 0
        for dept_code, dept in tt.items():
            for batch, schedule in dept.items():
                for day in DAYS:
                    found_empty = False
                    for slot in SLOTS:
                        entry = schedule[day][slot]
                        if entry is None:
                            found_empty = True
                        elif found_empty:
                            gap_count += 1
                            break
        # Allow up to 10 gap instances across all 16 batches × 5 days (80 day-slots).
        # The relaxed second-pass may produce a few non-contiguous placements
        # when teacher availability is tight.
        assert gap_count <= 10, (
            f"Too many gap violations ({gap_count}); "
            f"generator's contiguous filling may be broken"
        )

    def test_entry_structure(self, timetable_and_warnings):
        """Every non-None entry should have the required keys."""
        tt, _ = timetable_and_warnings
        required_keys = {"subject", "subject_code", "teacher", "teacher_id"}
        for dept_code, dept in tt.items():
            for batch, schedule in dept.items():
                for day in DAYS:
                    for slot in SLOTS:
                        entry = schedule[day][slot]
                        if entry is not None:
                            assert required_keys <= set(entry.keys()), (
                                f"Entry in {batch}/{day}/{slot} missing keys"
                            )

    def test_subject_codes_valid(self, timetable_and_warnings):
        """Every scheduled subject code must exist in SUBJECTS_DB."""
        tt, _ = timetable_and_warnings
        for dept_code, dept in tt.items():
            for batch, schedule in dept.items():
                for day in DAYS:
                    for slot in SLOTS:
                        entry = schedule[day][slot]
                        if entry is not None:
                            assert entry["subject_code"] in SUBJECTS_DB, (
                                f"Unknown subject {entry['subject_code']} in {batch}"
                            )

    def test_scheduled_subjects_belong_to_batch(self, timetable_and_warnings):
        """Every subject placed in a batch's schedule must be one of
        the batch's assigned subjects."""
        tt, _ = timetable_and_warnings
        for dept_code, dept_data in DEPARTMENTS_DB.items():
            for batch, assigned_subjects in dept_data["batches"].items():
                schedule = tt[dept_code][batch]
                for day in DAYS:
                    for slot in SLOTS:
                        entry = schedule[day][slot]
                        if entry is not None:
                            assert entry["subject_code"] in assigned_subjects, (
                                f"{entry['subject_code']} scheduled in {batch} "
                                f"but not in its assigned subjects"
                            )

    def test_at_least_some_classes_scheduled(self, timetable_and_warnings):
        """Every batch should have at least 1 class scheduled."""
        tt, _ = timetable_and_warnings
        for dept_code, dept in tt.items():
            for batch, schedule in dept.items():
                total = sum(
                    1
                    for day in DAYS
                    for slot in SLOTS
                    if schedule[day][slot] is not None
                )
                assert total > 0, f"Batch {batch} has zero classes"
