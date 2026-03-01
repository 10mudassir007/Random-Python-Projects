"""
Subject / course catalogue.

Credit hours = contact hours per week.  Batches carry varying numbers of
subjects so daily class counts differ naturally across the week.
"""

SUBJECTS_DB = {
    # ── Computer Science ─────────────────────────────────────────────────────
    "CS101":   {"name": "Intro to Programming",      "credits": 3, "hours": 3},
    "CS201":   {"name": "Data Structures",            "credits": 3, "hours": 3},
    "CS301":   {"name": "Algorithms",                 "credits": 3, "hours": 3},
    "CS401":   {"name": "Operating Systems",          "credits": 3, "hours": 3},
    "CS501":   {"name": "Computer Networks",          "credits": 3, "hours": 3},
    "AI401":   {"name": "Artificial Intelligence",    "credits": 3, "hours": 3},
    "DB301":   {"name": "Database Systems",           "credits": 3, "hours": 3},
    "ML401":   {"name": "Machine Learning",           "credits": 3, "hours": 3},
    # ── Software Engineering ─────────────────────────────────────────────────
    "SE201":   {"name": "Software Engineering",       "credits": 3, "hours": 3},
    "SE301":   {"name": "Software Design Patterns",   "credits": 3, "hours": 3},
    "SE401":   {"name": "Software Project Mgmt",      "credits": 3, "hours": 3},
    "SE501":   {"name": "Software Testing & QA",      "credits": 3, "hours": 3},
    # ── Electrical Engineering ───────────────────────────────────────────────
    "EE101":   {"name": "Circuit Theory",             "credits": 3, "hours": 3},
    "EE201":   {"name": "Electronics",                "credits": 3, "hours": 3},
    "EE301":   {"name": "Signals & Systems",          "credits": 3, "hours": 3},
    "EE401":   {"name": "Power Systems",              "credits": 3, "hours": 3},
    "EE501":   {"name": "Control Systems",            "credits": 3, "hours": 3},
    "EE601":   {"name": "Digital Logic Design",       "credits": 3, "hours": 3},
    # ── Mathematics / Statistics ─────────────────────────────────────────────
    "MATH101": {"name": "Calculus I",                 "credits": 3, "hours": 3},
    "MATH201": {"name": "Calculus II",                "credits": 3, "hours": 3},
    "MATH301": {"name": "Linear Algebra",             "credits": 3, "hours": 3},
    "MATH401": {"name": "Differential Equations",     "credits": 3, "hours": 3},
    "STAT301": {"name": "Statistics & Probability",   "credits": 3, "hours": 3},
    # ── Physics ──────────────────────────────────────────────────────────────
    "PHY101":  {"name": "Physics I",                  "credits": 3, "hours": 3},
    "PHY201":  {"name": "Physics II",                 "credits": 3, "hours": 3},
    "PHY301":  {"name": "Modern Physics",             "credits": 3, "hours": 3},
    # ── Business / Management ────────────────────────────────────────────────
    "BUS101":  {"name": "Business Communication",     "credits": 3, "hours": 3},
    "BUS201":  {"name": "Principles of Marketing",    "credits": 3, "hours": 3},
    "BUS301":  {"name": "Financial Accounting",       "credits": 3, "hours": 3},
    "BUS401":  {"name": "Business Strategy",          "credits": 3, "hours": 3},
    "BUS501":  {"name": "Entrepreneurship",           "credits": 3, "hours": 3},
    "MGT201":  {"name": "Organizational Behavior",    "credits": 3, "hours": 3},
    "MGT301":  {"name": "Human Resource Mgmt",        "credits": 3, "hours": 3},
    "MGT401":  {"name": "Strategic Management",       "credits": 3, "hours": 3},
    "FIN301":  {"name": "Corporate Finance",          "credits": 3, "hours": 3},
    "FIN401":  {"name": "Investment Analysis",        "credits": 3, "hours": 3},
    # ── English / Humanities / General ───────────────────────────────────────
    "ENG101":  {"name": "English Composition",        "credits": 3, "hours": 3},
    "ENG201":  {"name": "Technical Writing",          "credits": 3, "hours": 3},
    "HUM201":  {"name": "Ethics & Society",           "credits": 2, "hours": 2},
    "HUM301":  {"name": "Pakistan Studies",           "credits": 2, "hours": 2},
    "ISL101":  {"name": "Islamic Studies",            "credits": 2, "hours": 2},
}
