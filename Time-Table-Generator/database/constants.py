"""Time-slot and day constants."""

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Teaching slots — classes start at 08:30.
# A 30-minute break falls at 10:30-11:00 (between slot 2 and slot 3).
SLOTS = [
    "08:30-09:30",
    "09:30-10:30",
    # ── 10:30 - 11:00  BREAK ──
    "11:00-12:00",
    "12:00-13:00",
    "13:00-14:00",
    "14:00-15:00",
    "15:00-16:00",
]

# Index after which the break occurs (0-based).
# The break sits between SLOTS[1] and SLOTS[2].
BREAK_AFTER = 1
BREAK_LABEL = "10:30-11:00"
