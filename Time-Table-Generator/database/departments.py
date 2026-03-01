"""
Department and batch definitions.

Each batch carries 5-6 subjects with varying credit hours (2 or 3).
Total weekly hours per batch are NOT fixed — they vary naturally
(e.g. 16, 17, or 18 hours), so some days are busier than others.
"""

DEPARTMENTS_DB = {
    "CS": {
        "name": "Computer Science",
        "batches": {
            "CS-1A": ["CS101", "MATH101", "PHY101", "ENG101", "ISL101", "SE201"],
            "CS-2A": ["CS201", "MATH201", "ENG201", "DB301", "CS501", "HUM201"],
            "CS-3A": ["CS301", "CS401", "SE401", "STAT301", "AI401", "HUM301"],
            "CS-4A": ["AI401", "ML401", "HUM301", "DB301", "SE501", "MATH401"],
        },
    },
    "SE": {
        "name": "Software Engineering",
        "batches": {
            "SE-1A": ["CS101", "MATH101", "ENG101", "SE201", "ISL101", "PHY101"],
            "SE-2A": ["CS201", "SE301", "DB301", "ENG201", "MATH201", "HUM201"],
            "SE-3A": ["CS301", "SE401", "HUM201", "STAT301", "AI401", "MATH301"],
            "SE-4A": ["AI401", "SE401", "MGT301", "CS401", "ML401", "HUM301"],
        },
    },
    "EE": {
        "name": "Electrical Engineering",
        "batches": {
            "EE-1A": ["EE101", "MATH101", "PHY101", "ENG101", "ISL101", "EE601"],
            "EE-2A": ["EE201", "MATH201", "PHY201", "ENG201", "EE501", "HUM201"],
            "EE-3A": ["EE301", "EE401", "STAT301", "HUM201", "MATH301", "EE501"],
            "EE-4A": ["EE401", "MATH301", "MGT401", "HUM301", "EE601", "PHY301"],
        },
    },
    "BBA": {
        "name": "Business Administration",
        "batches": {
            "BBA-1A": ["BUS101", "MATH101", "ENG101", "MGT201", "ISL101", "HUM201"],
            "BBA-2A": ["BUS201", "BUS301", "ENG201", "MGT301", "FIN301", "HUM301"],
            "BBA-3A": ["BUS401", "MGT301", "HUM201", "STAT301", "FIN401", "BUS501"],
            "BBA-4A": ["MGT201", "MGT401", "HUM301", "BUS301", "FIN301", "ISL101"],
        },
    },
}
