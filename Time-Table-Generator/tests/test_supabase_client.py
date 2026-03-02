"""
Tests for the Supabase client module.
Uses mocking so no real Supabase connection is needed.
"""

import pytest
from unittest.mock import patch, MagicMock
from database.supabase_client import (
    fetch_teachers,
    fetch_subjects,
    fetch_departments,
    _get_client,
)


# ─────────────────────────────────────────────────────────────────────────────
# _get_client
# ─────────────────────────────────────────────────────────────────────────────

class TestGetClient:
    @patch("database.supabase_client.SUPABASE_URL", "")
    @patch("database.supabase_client.SUPABASE_KEY", "")
    def test_raises_on_empty_creds(self):
        with pytest.raises(ValueError, match="empty"):
            _get_client()

    @patch("database.supabase_client.SUPABASE_URL", "https://example.supabase.co")
    @patch("database.supabase_client.SUPABASE_KEY", "")
    def test_raises_on_empty_key(self):
        with pytest.raises(ValueError, match="empty"):
            _get_client()

    @patch("database.supabase_client.SUPABASE_URL", "")
    @patch("database.supabase_client.SUPABASE_KEY", "some-key")
    def test_raises_on_empty_url(self):
        with pytest.raises(ValueError, match="empty"):
            _get_client()


# ─────────────────────────────────────────────────────────────────────────────
# Helpers for mocking Supabase responses
# ─────────────────────────────────────────────────────────────────────────────

def _mock_client(table_data: dict) -> MagicMock:
    """
    Create a mock Supabase client.

    table_data = { "teachers": [...], "subjects": [...], ... }
    client.table("teachers").select("*").execute().data → table_data["teachers"]
    """
    client = MagicMock()

    def table_side_effect(name):
        t = MagicMock()
        resp = MagicMock()
        resp.data = table_data.get(name, [])
        t.select.return_value.execute.return_value = resp
        return t

    client.table.side_effect = table_side_effect
    return client


# ─────────────────────────────────────────────────────────────────────────────
# fetch_teachers
# ─────────────────────────────────────────────────────────────────────────────

class TestFetchTeachers:
    def test_basic(self):
        client = _mock_client({
            "teachers": [
                {"id": "T01", "name": "Dr. Test"},
                {"id": "T02", "name": "Prof. Mock"},
            ],
            "teacher_subjects": [
                {"teacher_id": "T01", "subject_code": "CS101"},
                {"teacher_id": "T01", "subject_code": "CS201"},
                {"teacher_id": "T02", "subject_code": "MATH101"},
            ],
        })
        result = fetch_teachers(client)

        assert "T01" in result
        assert result["T01"]["name"] == "Dr. Test"
        assert result["T01"]["can_teach"] == ["CS101", "CS201"]
        assert result["T02"]["can_teach"] == ["MATH101"]

    def test_teacher_with_no_subjects(self):
        """A teacher with no entries in junction table gets an empty list."""
        client = _mock_client({
            "teachers": [{"id": "T99", "name": "Dr. None"}],
            "teacher_subjects": [],
        })
        result = fetch_teachers(client)
        assert result["T99"]["can_teach"] == []

    def test_empty_teachers_table(self):
        client = _mock_client({"teachers": [], "teacher_subjects": []})
        result = fetch_teachers(client)
        assert result == {}


# ─────────────────────────────────────────────────────────────────────────────
# fetch_subjects
# ─────────────────────────────────────────────────────────────────────────────

class TestFetchSubjects:
    def test_basic(self):
        client = _mock_client({
            "subjects": [
                {"code": "CS101", "name": "Intro to Programming", "credits": 3, "hours": 3},
            ],
        })
        result = fetch_subjects(client)
        assert "CS101" in result
        assert result["CS101"]["name"] == "Intro to Programming"
        assert result["CS101"]["credits"] == 3
        assert result["CS101"]["hours"] == 3

    def test_empty_subjects_table(self):
        client = _mock_client({"subjects": []})
        result = fetch_subjects(client)
        assert result == {}


# ─────────────────────────────────────────────────────────────────────────────
# fetch_departments
# ─────────────────────────────────────────────────────────────────────────────

class TestFetchDepartments:
    def test_basic(self):
        client = _mock_client({
            "departments": [
                {"dept_code": "CS", "dept_name": "Computer Science"},
            ],
            "batches": [
                {"batch": "CS-1A", "dept_code": "CS"},
                {"batch": "CS-2A", "dept_code": "CS"},
            ],
            "batch_subjects": [
                {"batch": "CS-1A", "subject_code": "CS101"},
                {"batch": "CS-1A", "subject_code": "MATH101"},
                {"batch": "CS-2A", "subject_code": "CS201"},
            ],
        })
        result = fetch_departments(client)

        assert "CS" in result
        assert result["CS"]["name"] == "Computer Science"
        assert "CS-1A" in result["CS"]["batches"]
        assert result["CS"]["batches"]["CS-1A"] == ["CS101", "MATH101"]
        assert result["CS"]["batches"]["CS-2A"] == ["CS201"]

    def test_multiple_departments(self):
        client = _mock_client({
            "departments": [
                {"dept_code": "CS", "dept_name": "Computer Science"},
                {"dept_code": "EE", "dept_name": "Electrical Engineering"},
            ],
            "batches": [
                {"batch": "CS-1A", "dept_code": "CS"},
                {"batch": "EE-1A", "dept_code": "EE"},
            ],
            "batch_subjects": [
                {"batch": "CS-1A", "subject_code": "CS101"},
                {"batch": "EE-1A", "subject_code": "EE101"},
            ],
        })
        result = fetch_departments(client)
        assert len(result) == 2
        assert "CS" in result and "EE" in result

    def test_batch_with_no_subjects(self):
        """A batch with no entries in the junction table gets an empty list."""
        client = _mock_client({
            "departments": [{"dept_code": "CS", "dept_name": "CS"}],
            "batches": [{"batch": "CS-1A", "dept_code": "CS"}],
            "batch_subjects": [],
        })
        result = fetch_departments(client)
        assert result["CS"]["batches"]["CS-1A"] == []

    def test_empty_tables(self):
        client = _mock_client({
            "departments": [],
            "batches": [],
            "batch_subjects": [],
        })
        result = fetch_departments(client)
        assert result == {}
