"""
Tests for the display / formatting module.
Validates that output strings are well-formed and contain expected content.
"""

import random
import pytest
from generator import generate_timetable
from display import format_batch_timetable, format_summary, _active_slots_for_day
from database import DAYS, SLOTS, DEPARTMENTS_DB


@pytest.fixture(scope="module")
def timetable():
    random.seed(42)
    tt, _ = generate_timetable()
    return tt


# ─────────────────────────────────────────────────────────────────────────────
# _active_slots_for_day
# ─────────────────────────────────────────────────────────────────────────────

class TestActiveSlots:
    def test_empty_day_returns_zero(self):
        schedule = {
            day: {slot: None for slot in SLOTS} for day in DAYS
        }
        assert _active_slots_for_day(schedule, "Monday") == 0

    def test_fully_filled_day(self):
        schedule = {
            day: {
                slot: {"subject": "X", "subject_code": "X", "teacher": "Y", "teacher_id": "T01"}
                for slot in SLOTS
            }
            for day in DAYS
        }
        assert _active_slots_for_day(schedule, "Monday") == len(SLOTS)

    def test_partial_fill_counts_contiguous(self):
        """Only contiguous filled slots from the top are counted."""
        schedule = {day: {slot: None for slot in SLOTS} for day in DAYS}
        entry = {"subject": "X", "subject_code": "X", "teacher": "Y", "teacher_id": "T01"}
        # Fill first 3 slots only
        for i in range(3):
            schedule["Monday"][SLOTS[i]] = entry
        assert _active_slots_for_day(schedule, "Monday") == 3

    def test_gap_stops_count(self):
        """A gap in the middle should stop the contiguous count."""
        schedule = {day: {slot: None for slot in SLOTS} for day in DAYS}
        entry = {"subject": "X", "subject_code": "X", "teacher": "Y", "teacher_id": "T01"}
        # Fill slot 0 and slot 2, leave slot 1 empty
        schedule["Monday"][SLOTS[0]] = entry
        # slot 1 is None
        schedule["Monday"][SLOTS[2]] = entry
        assert _active_slots_for_day(schedule, "Monday") == 1


# ─────────────────────────────────────────────────────────────────────────────
# format_batch_timetable
# ─────────────────────────────────────────────────────────────────────────────

class TestFormatBatchTimetable:
    def test_returns_string(self, timetable):
        dept_code = list(timetable.keys())[0]
        dept_name = DEPARTMENTS_DB[dept_code]["name"]
        batch = list(timetable[dept_code].keys())[0]
        schedule = timetable[dept_code][batch]
        result = format_batch_timetable(dept_name, batch, schedule)
        assert isinstance(result, str)

    def test_contains_department_name(self, timetable):
        dept_code = list(timetable.keys())[0]
        dept_name = DEPARTMENTS_DB[dept_code]["name"]
        batch = list(timetable[dept_code].keys())[0]
        schedule = timetable[dept_code][batch]
        result = format_batch_timetable(dept_name, batch, schedule)
        assert dept_name in result

    def test_contains_batch_name(self, timetable):
        dept_code = list(timetable.keys())[0]
        batch = list(timetable[dept_code].keys())[0]
        dept_name = DEPARTMENTS_DB[dept_code]["name"]
        schedule = timetable[dept_code][batch]
        result = format_batch_timetable(dept_name, batch, schedule)
        assert batch in result

    def test_contains_day_headers(self, timetable):
        dept_code = list(timetable.keys())[0]
        batch = list(timetable[dept_code].keys())[0]
        dept_name = DEPARTMENTS_DB[dept_code]["name"]
        schedule = timetable[dept_code][batch]
        result = format_batch_timetable(dept_name, batch, schedule)
        for day in DAYS:
            assert day in result

    def test_contains_break_label(self, timetable):
        """The BREAK row should appear in timetables with >2 slots."""
        dept_code = list(timetable.keys())[0]
        batch = list(timetable[dept_code].keys())[0]
        dept_name = DEPARTMENTS_DB[dept_code]["name"]
        schedule = timetable[dept_code][batch]
        result = format_batch_timetable(dept_name, batch, schedule)
        assert "BREAK" in result

    def test_contains_subject_teacher_mapping(self, timetable):
        """Output should contain 'Subject' and 'Teacher' headers for the mapping."""
        dept_code = list(timetable.keys())[0]
        batch = list(timetable[dept_code].keys())[0]
        dept_name = DEPARTMENTS_DB[dept_code]["name"]
        schedule = timetable[dept_code][batch]
        result = format_batch_timetable(dept_name, batch, schedule)
        assert "Subject" in result
        assert "Teacher" in result

    def test_contains_total_count(self, timetable):
        dept_code = list(timetable.keys())[0]
        batch = list(timetable[dept_code].keys())[0]
        dept_name = DEPARTMENTS_DB[dept_code]["name"]
        schedule = timetable[dept_code][batch]
        result = format_batch_timetable(dept_name, batch, schedule)
        assert "Total:" in result


# ─────────────────────────────────────────────────────────────────────────────
# format_summary
# ─────────────────────────────────────────────────────────────────────────────

class TestFormatSummary:
    def test_returns_string(self, timetable):
        result = format_summary(timetable)
        assert isinstance(result, str)

    def test_contains_summary_header(self, timetable):
        result = format_summary(timetable)
        assert "SUMMARY" in result

    def test_contains_all_departments(self, timetable):
        result = format_summary(timetable)
        for dept_code in DEPARTMENTS_DB:
            assert dept_code in result

    def test_contains_hrs_week(self, timetable):
        result = format_summary(timetable)
        assert "hrs/week" in result
