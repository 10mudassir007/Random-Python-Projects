"""
Tests for database constants, teachers, subjects, and departments.
Validates data integrity and structure of the hardcoded data.
"""

import pytest
from database.constants import DAYS, SLOTS, BREAK_AFTER, BREAK_LABEL
from database.teachers import TEACHERS_DB
from database.subjects import SUBJECTS_DB
from database.departments import DEPARTMENTS_DB


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

class TestConstants:
    def test_days_count(self):
        assert len(DAYS) == 5

    def test_days_are_weekdays(self):
        expected = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        assert DAYS == expected

    def test_slots_not_empty(self):
        assert len(SLOTS) >= 5

    def test_slots_are_strings(self):
        for slot in SLOTS:
            assert isinstance(slot, str)

    def test_slot_format(self):
        """Each slot should look like HH:MM-HH:MM."""
        for slot in SLOTS:
            parts = slot.split("-")
            assert len(parts) == 2
            for part in parts:
                hh, mm = part.split(":")
                assert hh.isdigit() and mm.isdigit()

    def test_break_after_is_valid_index(self):
        assert 0 <= BREAK_AFTER < len(SLOTS) - 1

    def test_break_label_format(self):
        assert "-" in BREAK_LABEL
        assert ":" in BREAK_LABEL


# ─────────────────────────────────────────────────────────────────────────────
# Teachers
# ─────────────────────────────────────────────────────────────────────────────

class TestTeachers:
    def test_teachers_not_empty(self):
        assert len(TEACHERS_DB) > 0

    def test_teacher_has_required_keys(self):
        for tid, data in TEACHERS_DB.items():
            assert "name" in data, f"Teacher {tid} missing 'name'"
            assert "can_teach" in data, f"Teacher {tid} missing 'can_teach'"

    def test_teacher_id_format(self):
        """All teacher IDs should start with 'T' followed by digits."""
        for tid in TEACHERS_DB:
            assert tid.startswith("T"), f"Teacher ID {tid} doesn't start with 'T'"
            assert tid[1:].isdigit(), f"Teacher ID {tid} has non-digit suffix"

    def test_teacher_name_is_string(self):
        for tid, data in TEACHERS_DB.items():
            assert isinstance(data["name"], str)
            assert len(data["name"]) > 0

    def test_teacher_can_teach_is_list(self):
        for tid, data in TEACHERS_DB.items():
            assert isinstance(data["can_teach"], list)
            assert len(data["can_teach"]) > 0, f"Teacher {tid} can't teach anything"

    def test_teacher_subjects_exist_in_subjects_db(self):
        """Every subject a teacher can teach must exist in SUBJECTS_DB."""
        for tid, data in TEACHERS_DB.items():
            for subj in data["can_teach"]:
                assert subj in SUBJECTS_DB, (
                    f"Teacher {tid} lists subject '{subj}' which doesn't exist"
                )


# ─────────────────────────────────────────────────────────────────────────────
# Subjects
# ─────────────────────────────────────────────────────────────────────────────

class TestSubjects:
    def test_subjects_not_empty(self):
        assert len(SUBJECTS_DB) > 0

    def test_subject_has_required_keys(self):
        for code, data in SUBJECTS_DB.items():
            assert "name" in data, f"Subject {code} missing 'name'"
            assert "credits" in data, f"Subject {code} missing 'credits'"
            assert "hours" in data, f"Subject {code} missing 'hours'"

    def test_credits_positive(self):
        for code, data in SUBJECTS_DB.items():
            assert data["credits"] > 0, f"Subject {code} has non-positive credits"

    def test_hours_positive(self):
        for code, data in SUBJECTS_DB.items():
            assert data["hours"] > 0, f"Subject {code} has non-positive hours"

    def test_hours_not_exceed_days(self):
        """A subject's weekly hours should not exceed the number of days."""
        for code, data in SUBJECTS_DB.items():
            assert data["hours"] <= len(DAYS), (
                f"Subject {code} has {data['hours']} hours, more than {len(DAYS)} days"
            )


# ─────────────────────────────────────────────────────────────────────────────
# Departments
# ─────────────────────────────────────────────────────────────────────────────

class TestDepartments:
    def test_departments_not_empty(self):
        assert len(DEPARTMENTS_DB) > 0

    def test_department_has_required_keys(self):
        for code, data in DEPARTMENTS_DB.items():
            assert "name" in data, f"Dept {code} missing 'name'"
            assert "batches" in data, f"Dept {code} missing 'batches'"

    def test_each_department_has_batches(self):
        for code, data in DEPARTMENTS_DB.items():
            assert len(data["batches"]) > 0, f"Dept {code} has no batches"

    def test_batch_subjects_are_lists(self):
        for code, data in DEPARTMENTS_DB.items():
            for batch, subjects in data["batches"].items():
                assert isinstance(subjects, list), (
                    f"Batch {batch} subjects is not a list"
                )
                assert len(subjects) > 0, f"Batch {batch} has no subjects"

    def test_batch_subjects_exist_in_subjects_db(self):
        """Every subject code in a batch must exist in SUBJECTS_DB."""
        for code, data in DEPARTMENTS_DB.items():
            for batch, subjects in data["batches"].items():
                for subj in subjects:
                    assert subj in SUBJECTS_DB, (
                        f"Batch {batch} lists subject '{subj}' which doesn't exist"
                    )

    def test_every_batch_subject_has_at_least_one_teacher(self):
        """For every subject in every batch, at least one teacher can teach it."""
        all_teachable = set()
        for tid, data in TEACHERS_DB.items():
            all_teachable.update(data["can_teach"])

        for code, data in DEPARTMENTS_DB.items():
            for batch, subjects in data["batches"].items():
                for subj in subjects:
                    assert subj in all_teachable, (
                        f"No teacher can teach '{subj}' needed by batch {batch}"
                    )
