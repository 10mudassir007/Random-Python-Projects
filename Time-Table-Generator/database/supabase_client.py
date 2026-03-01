"""
Supabase client — fetches from the normalized 6-table schema and
reconstructs the same dict format the hardcoded modules use.

Tables queried:
    teachers, subjects, departments, batches,
    teacher_subjects (junction), batch_subjects (junction)

Required environment variables (in .env):
    SUPABASE_URL   – your Supabase project URL
    SUPABASE_KEY   – anon or service-role key
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")


def _get_client() -> Client:
    """Create and return a Supabase client.  Raises on bad / missing creds."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL or SUPABASE_KEY is empty.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


# ─────────────────────────────────────────────────────────────────────────────
# Public loaders — each returns the same shape as the hardcoded dicts
# ─────────────────────────────────────────────────────────────────────────────

def fetch_teachers(client: Client) -> dict:
    """
    Fetch from `teachers` + `teacher_subjects` junction table.

    Returns:  { "T01": {"name": "...", "can_teach": ["CS101", ...]}, ... }
    """
    teacher_rows = client.table("teachers").select("*").execute().data
    ts_rows = client.table("teacher_subjects").select("*").execute().data

    # Build teacher_id → [subject_codes] from the junction table
    teach_map: dict[str, list[str]] = {}
    for row in ts_rows:
        teach_map.setdefault(row["teacher_id"], []).append(row["subject_code"])

    return {
        row["id"]: {
            "name": row["name"],
            "can_teach": teach_map.get(row["id"], []),
        }
        for row in teacher_rows
    }


def fetch_subjects(client: Client) -> dict:
    """
    Fetch from the `subjects` table (unchanged — already normalized).

    Returns:  { "CS101": {"name": "...", "credits": 3, "hours": 3}, ... }
    """
    rows = client.table("subjects").select("*").execute().data
    return {
        row["code"]: {
            "name": row["name"],
            "credits": row["credits"],
            "hours": row["hours"],
        }
        for row in rows
    }


def fetch_departments(client: Client) -> dict:
    """
    Fetch from `departments` + `batches` + `batch_subjects` junction table.

    Returns the nested dict the generator expects:
        {
            "CS": {
                "name": "Computer Science",
                "batches": {
                    "CS-1A": ["CS101", ...],
                    ...
                }
            },
            ...
        }
    """
    dept_rows = client.table("departments").select("*").execute().data
    batch_rows = client.table("batches").select("*").execute().data
    bs_rows = client.table("batch_subjects").select("*").execute().data

    # Build batch → [subject_codes] from the junction table
    batch_subj_map: dict[str, list[str]] = {}
    for row in bs_rows:
        batch_subj_map.setdefault(row["batch"], []).append(row["subject_code"])

    # Build dept_code → dept_name lookup
    dept_names = {row["dept_code"]: row["dept_name"] for row in dept_rows}

    # Assemble the nested dict from batches table
    departments: dict = {}
    for row in batch_rows:
        dc = row["dept_code"]
        if dc not in departments:
            departments[dc] = {
                "name": dept_names.get(dc, dc),
                "batches": {},
            }
        departments[dc]["batches"][row["batch"]] = batch_subj_map.get(row["batch"], [])

    return departments


def load_all_from_supabase() -> tuple[dict, dict, dict]:
    """
    Convenience wrapper — fetches teachers, subjects, and departments
    in one call.

    Returns
    -------
    (TEACHERS_DB, SUBJECTS_DB, DEPARTMENTS_DB)

    Raises on any connection / query failure so the caller can fall back.
    """
    client = _get_client()
    teachers = fetch_teachers(client)
    subjects = fetch_subjects(client)
    departments = fetch_departments(client)
    return teachers, subjects, departments
