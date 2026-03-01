"""
Simulated university database — teachers, subjects, departments.
"""

from .teachers import TEACHERS_DB
from .subjects import SUBJECTS_DB
from .departments import DEPARTMENTS_DB
from .constants import DAYS, SLOTS, BREAK_AFTER, BREAK_LABEL

__all__ = [
    "TEACHERS_DB",
    "SUBJECTS_DB",
    "DEPARTMENTS_DB",
    "DAYS",
    "SLOTS",
    "BREAK_AFTER",
    "BREAK_LABEL",
]
