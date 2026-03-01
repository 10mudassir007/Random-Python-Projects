"""
Teacher records.

Enough teachers so that every slot across all 16 batches can be filled
without conflicts.  Each teacher can teach up to 40 slots/week (5 days × 8).
"""

TEACHERS_DB = {
    # ── Computer Science teachers ────────────────────────────────────────────
    "T01": {"name": "Dr. Ayesha Malik",         "can_teach": ["CS101", "CS201", "CS301", "AI401"]},
    "T02": {"name": "Prof. Zubair Ahmed",       "can_teach": ["CS201", "CS401", "SE301", "SE401"]},
    "T08": {"name": "Dr. Omar Farhan",          "can_teach": ["CS301", "CS401", "AI401", "DB301"]},
    "T09": {"name": "Mr. Bilal Hussain",        "can_teach": ["SE201", "SE301", "DB301", "CS201"]},
    "T13": {"name": "Dr. Kamran Ali",           "can_teach": ["CS101", "CS201", "CS501", "DB301"]},
    "T14": {"name": "Ms. Mehwish Noor",         "can_teach": ["AI401", "ML401", "CS301", "STAT301"]},
    "T15": {"name": "Dr. Farooq Azam",          "can_teach": ["CS401", "CS501", "SE401", "SE501"]},
    "T16": {"name": "Mr. Usman Ghani",          "can_teach": ["ML401", "AI401", "DB301", "CS501"]},
    "T17": {"name": "Dr. Hira Batool",          "can_teach": ["SE201", "SE301", "SE401", "SE501"]},
    "T18": {"name": "Prof. Adeel Rauf",         "can_teach": ["CS101", "SE201", "SE501", "DB301"]},

    # ── Mathematics / Statistics teachers ────────────────────────────────────
    "T03": {"name": "Dr. Sara Khan",            "can_teach": ["MATH101", "MATH201", "STAT301"]},
    "T11": {"name": "Prof. Tariq Mehmood",      "can_teach": ["MATH101", "MATH201", "MATH301", "STAT301"]},
    "T19": {"name": "Dr. Amna Siddiqui",        "can_teach": ["MATH301", "MATH401", "STAT301"]},
    "T20": {"name": "Mr. Waqar Haider",         "can_teach": ["MATH101", "MATH201", "MATH401"]},
    "T21": {"name": "Dr. Lubna Rafiq",          "can_teach": ["STAT301", "MATH301", "MATH401", "MATH201"]},

    # ── Physics teachers ─────────────────────────────────────────────────────
    "T04": {"name": "Mr. Hassan Raza",          "can_teach": ["PHY101", "PHY201", "EE201"]},
    "T22": {"name": "Dr. Asad Mehmood",         "can_teach": ["PHY101", "PHY201", "PHY301"]},
    "T23": {"name": "Ms. Samra Iqbal",          "can_teach": ["PHY101", "PHY201", "PHY301"]},

    # ── Electrical Engineering teachers ──────────────────────────────────────
    "T05": {"name": "Dr. Nadia Farooq",         "can_teach": ["EE101", "EE201", "EE301", "EE401"]},
    "T24": {"name": "Prof. Zahid Hussain",      "can_teach": ["EE301", "EE401", "EE501", "EE601"]},
    "T25": {"name": "Dr. Sadia Anwar",          "can_teach": ["EE101", "EE201", "EE501", "EE601"]},
    "T26": {"name": "Mr. Faizan Akram",         "can_teach": ["EE401", "EE501", "EE601", "PHY301"]},

    # ── Business / Management teachers ───────────────────────────────────────
    "T06": {"name": "Prof. Imran Siddiqui",     "can_teach": ["BUS101", "BUS201", "MGT301", "MGT401"]},
    "T10": {"name": "Dr. Rabia Qureshi",        "can_teach": ["MGT201", "MGT301", "BUS301", "BUS401"]},
    "T27": {"name": "Dr. Fahad Mirza",          "can_teach": ["FIN301", "FIN401", "BUS401", "BUS501"]},
    "T28": {"name": "Ms. Alina Tariq",          "can_teach": ["BUS101", "BUS201", "BUS501", "MGT201"]},
    "T29": {"name": "Prof. Nadeem Shah",        "can_teach": ["MGT301", "MGT401", "FIN301", "FIN401"]},
    "T30": {"name": "Dr. Sana Pervez",          "can_teach": ["BUS301", "BUS401", "BUS501", "FIN301"]},

    # ── English / Humanities / General teachers ──────────────────────────────
    "T07": {"name": "Ms. Fatima Iqbal",         "can_teach": ["ENG101", "ENG201", "HUM301"]},
    "T12": {"name": "Ms. Saba Nawaz",           "can_teach": ["ENG101", "ENG201", "HUM201", "HUM301"]},
    "T31": {"name": "Dr. Rizwan Qamar",         "can_teach": ["ENG101", "ENG201", "ISL101"]},
    "T32": {"name": "Prof. Tahira Begum",       "can_teach": ["HUM201", "HUM301", "ISL101", "ENG101"]},
    "T33": {"name": "Mr. Junaid Saeed",         "can_teach": ["ISL101", "HUM201", "HUM301"]},
    "T34": {"name": "Ms. Nargis Akhtar",        "can_teach": ["ENG101", "ENG201", "HUM201", "ISL101"]},
    "T35": {"name": "Dr. Khalid Mehmood",       "can_teach": ["ENG101", "ENG201", "HUM301", "ISL101"]},
    "T36": {"name": "Ms. Raheela Aslam",        "can_teach": ["ENG201", "HUM201", "HUM301", "ISL101"]},
    "T37": {"name": "Mr. Naveed Iqbal",         "can_teach": ["DB301", "CS201", "CS501", "SE301"]},
    "T38": {"name": "Dr. Saima Jabeen",         "can_teach": ["STAT301", "MATH201", "MATH301", "HUM201"]},
}
