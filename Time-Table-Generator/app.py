"""
University Timetable Generator
================================
Simulates a university database with:
- Multiple Departments
- Multiple Teachers (can teach multiple subjects)
- Each Department has 4 batches/classes
- Each batch has its own subjects
- Timetable is generated avoiding teacher conflicts

Project structure
-----------------
  database/          Simulated DB (teachers, subjects, departments, constants)
  generator/         Scheduling engine
  display/           Pretty-printing utilities
  app.py             Entry point (this file)
"""

import random

from database import DEPARTMENTS_DB
from generator import generate_timetable
from display import format_batch_timetable,  format_summary


def main():
    random.seed(42)  # reproducible output; remove for fresh randomness

    print("\n" + "=" * 120)
    print(" " * 40 + "UNIVERSITY TIMETABLE GENERATOR")
    print(" " * 38 + "Automated Scheduling System v2.0")
    print("=" * 120 + "\n")

    print("  Generating timetable...\n")
    timetable, warnings = generate_timetable()

    # ── Print warnings ───────────────────────────────────────────────────────
    if warnings:
        for w in warnings:
            print(f"  [WARN] {w}")
        print()

    # ── Per-batch timetables ─────────────────────────────────────────────────
    print("\n" + "=" * 120)
    print(" " * 45 + "BATCH-WISE TIMETABLES")
    print("=" * 120 + "\n")

    for dept_code, dept in timetable.items():
        dept_name = DEPARTMENTS_DB[dept_code]["name"]
        for batch, schedule in dept.items():
            print(format_batch_timetable(dept_name, batch, schedule))

    # ── Teacher-wise overview ────────────────────────────────────────────────
    # print("\n" + "=" * 120)
    # print(" " * 43 + "TEACHER-WISE SCHEDULES")
    # print("=" * 120 + "\n")
    # print(format_teacher_schedule(timetable))

    # # ── Summary ──────────────────────────────────────────────────────────────
    # print(format_summary(timetable))

    print("  Done! Timetable generated successfully.")
    print("=" * 120 + "\n")


if __name__ == "__main__":
    main()