"""
University database layer.

Tries to load teachers, subjects, and departments from Supabase.
If the connection fails (missing creds, network error, empty tables, etc.)
it falls back silently to the hardcoded data in the local modules.

Constants (DAYS, SLOTS, BREAK_*) are always local — they don't live in the DB.
"""

from .constants import DAYS, SLOTS, BREAK_AFTER, BREAK_LABEL

# ── Hardcoded fallback data ──────────────────────────────────────────────────
from .teachers import TEACHERS_DB as _TEACHERS_HARDCODED
from .subjects import SUBJECTS_DB as _SUBJECTS_HARDCODED
from .departments import DEPARTMENTS_DB as _DEPARTMENTS_HARDCODED

# ── Try Supabase first ───────────────────────────────────────────────────────
DATA_SOURCE: str = "hardcoded"   # will be overwritten on success

try:
    from .supabase_client import load_all_from_supabase

    _teachers, _subjects, _departments = load_all_from_supabase()

    # Only accept Supabase data if all three tables returned something
    if _teachers and _subjects and _departments:
        TEACHERS_DB = _teachers
        SUBJECTS_DB = _subjects
        DEPARTMENTS_DB = _departments
        DATA_SOURCE = "supabase"
    else:
        raise ValueError("One or more Supabase tables returned empty data.")

except Exception as exc:
    print(f"  [ERROR] Failed to load from Supabase: {exc}")
    # Any failure → fall back to hardcoded data
    TEACHERS_DB = _TEACHERS_HARDCODED
    SUBJECTS_DB = _SUBJECTS_HARDCODED
    DEPARTMENTS_DB = _DEPARTMENTS_HARDCODED
    DATA_SOURCE = "hardcoded"

__all__ = [
    "TEACHERS_DB",
    "SUBJECTS_DB",
    "DEPARTMENTS_DB",
    "DAYS",
    "SLOTS",
    "BREAK_AFTER",
    "BREAK_LABEL",
    "DATA_SOURCE",
]
