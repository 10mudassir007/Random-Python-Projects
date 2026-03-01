-- ============================================================================
-- Supabase schema for the Timetable Generator (NORMALIZED — 3NF)
-- Run this in the Supabase SQL Editor to create the required tables.
-- ============================================================================

-- Drop existing tables if re-running
DROP TABLE IF EXISTS batch_subjects CASCADE;
DROP TABLE IF EXISTS teacher_subjects CASCADE;
DROP TABLE IF EXISTS batches CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS teachers CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;

-- ============================================================================
-- CORE TABLES
-- ============================================================================

CREATE TABLE teachers (
    id      TEXT PRIMARY KEY,
    name    TEXT NOT NULL
);

CREATE TABLE subjects (
    code    TEXT PRIMARY KEY,
    name    TEXT NOT NULL,
    credits INTEGER NOT NULL DEFAULT 3,
    hours   INTEGER NOT NULL DEFAULT 3
);

CREATE TABLE departments (
    dept_code   TEXT PRIMARY KEY,
    dept_name   TEXT NOT NULL
);

CREATE TABLE batches (
    batch       TEXT PRIMARY KEY,
    dept_code   TEXT NOT NULL REFERENCES departments(dept_code) ON DELETE CASCADE
);

-- ============================================================================
-- JUNCTION TABLES
-- ============================================================================

-- Which teacher can teach which subject
CREATE TABLE teacher_subjects (
    teacher_id      TEXT NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
    subject_code    TEXT NOT NULL REFERENCES subjects(code) ON DELETE CASCADE,
    PRIMARY KEY (teacher_id, subject_code)
);

-- Which batch has which subject
CREATE TABLE batch_subjects (
    batch           TEXT NOT NULL REFERENCES batches(batch) ON DELETE CASCADE,
    subject_code    TEXT NOT NULL REFERENCES subjects(code) ON DELETE CASCADE,
    PRIMARY KEY (batch, subject_code)
);

-- ============================================================================
-- INSERT DATA
-- ============================================================================

-- ── Teachers (38) ───────────────────────────────────────────────────────────
INSERT INTO teachers (id, name) VALUES
    ('T01', 'Dr. Ayesha Malik'),
    ('T02', 'Prof. Zubair Ahmed'),
    ('T03', 'Dr. Sara Khan'),
    ('T04', 'Mr. Hassan Raza'),
    ('T05', 'Dr. Nadia Farooq'),
    ('T06', 'Prof. Imran Siddiqui'),
    ('T07', 'Ms. Fatima Iqbal'),
    ('T08', 'Dr. Omar Farhan'),
    ('T09', 'Mr. Bilal Hussain'),
    ('T10', 'Dr. Rabia Qureshi'),
    ('T11', 'Prof. Tariq Mehmood'),
    ('T12', 'Ms. Saba Nawaz'),
    ('T13', 'Dr. Kamran Ali'),
    ('T14', 'Ms. Mehwish Noor'),
    ('T15', 'Dr. Farooq Azam'),
    ('T16', 'Mr. Usman Ghani'),
    ('T17', 'Dr. Hira Batool'),
    ('T18', 'Prof. Adeel Rauf'),
    ('T19', 'Dr. Amna Siddiqui'),
    ('T20', 'Mr. Waqar Haider'),
    ('T21', 'Dr. Lubna Rafiq'),
    ('T22', 'Dr. Asad Mehmood'),
    ('T23', 'Ms. Samra Iqbal'),
    ('T24', 'Prof. Zahid Hussain'),
    ('T25', 'Dr. Sadia Anwar'),
    ('T26', 'Mr. Faizan Akram'),
    ('T27', 'Dr. Fahad Mirza'),
    ('T28', 'Ms. Alina Tariq'),
    ('T29', 'Prof. Nadeem Shah'),
    ('T30', 'Dr. Sana Pervez'),
    ('T31', 'Dr. Rizwan Qamar'),
    ('T32', 'Prof. Tahira Begum'),
    ('T33', 'Mr. Junaid Saeed'),
    ('T34', 'Ms. Nargis Akhtar'),
    ('T35', 'Dr. Khalid Mehmood'),
    ('T36', 'Ms. Raheela Aslam'),
    ('T37', 'Mr. Naveed Iqbal'),
    ('T38', 'Dr. Saima Jabeen');

-- ── Subjects (40) ──────────────────────────────────────────────────────────
INSERT INTO subjects (code, name, credits, hours) VALUES
    ('CS101',   'Intro to Programming',      3, 3),
    ('CS201',   'Data Structures',            3, 3),
    ('CS301',   'Algorithms',                 3, 3),
    ('CS401',   'Operating Systems',          3, 3),
    ('CS501',   'Computer Networks',          3, 3),
    ('AI401',   'Artificial Intelligence',    3, 3),
    ('DB301',   'Database Systems',           3, 3),
    ('ML401',   'Machine Learning',           3, 3),
    ('SE201',   'Software Engineering',       3, 3),
    ('SE301',   'Software Design Patterns',   3, 3),
    ('SE401',   'Software Project Mgmt',      3, 3),
    ('SE501',   'Software Testing & QA',      3, 3),
    ('EE101',   'Circuit Theory',             3, 3),
    ('EE201',   'Electronics',                3, 3),
    ('EE301',   'Signals & Systems',          3, 3),
    ('EE401',   'Power Systems',              3, 3),
    ('EE501',   'Control Systems',            3, 3),
    ('EE601',   'Digital Logic Design',       3, 3),
    ('MATH101', 'Calculus I',                 3, 3),
    ('MATH201', 'Calculus II',                3, 3),
    ('MATH301', 'Linear Algebra',             3, 3),
    ('MATH401', 'Differential Equations',     3, 3),
    ('STAT301', 'Statistics & Probability',   3, 3),
    ('PHY101',  'Physics I',                  3, 3),
    ('PHY201',  'Physics II',                 3, 3),
    ('PHY301',  'Modern Physics',             3, 3),
    ('BUS101',  'Business Communication',     3, 3),
    ('BUS201',  'Principles of Marketing',    3, 3),
    ('BUS301',  'Financial Accounting',       3, 3),
    ('BUS401',  'Business Strategy',          3, 3),
    ('BUS501',  'Entrepreneurship',           3, 3),
    ('MGT201',  'Organizational Behavior',    3, 3),
    ('MGT301',  'Human Resource Mgmt',        3, 3),
    ('MGT401',  'Strategic Management',       3, 3),
    ('FIN301',  'Corporate Finance',          3, 3),
    ('FIN401',  'Investment Analysis',        3, 3),
    ('ENG101',  'English Composition',        3, 3),
    ('ENG201',  'Technical Writing',          3, 3),
    ('HUM201',  'Ethics & Society',           2, 2),
    ('HUM301',  'Pakistan Studies',           2, 2),
    ('ISL101',  'Islamic Studies',            2, 2);

-- ── Departments (4) ────────────────────────────────────────────────────────
INSERT INTO departments (dept_code, dept_name) VALUES
    ('CS',  'Computer Science'),
    ('SE',  'Software Engineering'),
    ('EE',  'Electrical Engineering'),
    ('BBA', 'Business Administration');

-- ── Batches (16) ───────────────────────────────────────────────────────────
INSERT INTO batches (batch, dept_code) VALUES
    ('CS-1A', 'CS'),  ('CS-2A', 'CS'),  ('CS-3A', 'CS'),  ('CS-4A', 'CS'),
    ('SE-1A', 'SE'),  ('SE-2A', 'SE'),  ('SE-3A', 'SE'),  ('SE-4A', 'SE'),
    ('EE-1A', 'EE'),  ('EE-2A', 'EE'),  ('EE-3A', 'EE'),  ('EE-4A', 'EE'),
    ('BBA-1A', 'BBA'), ('BBA-2A', 'BBA'), ('BBA-3A', 'BBA'), ('BBA-4A', 'BBA');

-- ── Teacher ↔ Subject mappings ─────────────────────────────────────────────
-- CS teachers
INSERT INTO teacher_subjects (teacher_id, subject_code) VALUES
    ('T01', 'CS101'), ('T01', 'CS201'), ('T01', 'CS301'), ('T01', 'AI401'),
    ('T02', 'CS201'), ('T02', 'CS401'), ('T02', 'SE301'), ('T02', 'SE401'),
    ('T08', 'CS301'), ('T08', 'CS401'), ('T08', 'AI401'), ('T08', 'DB301'),
    ('T09', 'SE201'), ('T09', 'SE301'), ('T09', 'DB301'), ('T09', 'CS201'),
    ('T13', 'CS101'), ('T13', 'CS201'), ('T13', 'CS501'), ('T13', 'DB301'),
    ('T14', 'AI401'), ('T14', 'ML401'), ('T14', 'CS301'), ('T14', 'STAT301'),
    ('T15', 'CS401'), ('T15', 'CS501'), ('T15', 'SE401'), ('T15', 'SE501'),
    ('T16', 'ML401'), ('T16', 'AI401'), ('T16', 'DB301'), ('T16', 'CS501'),
    ('T17', 'SE201'), ('T17', 'SE301'), ('T17', 'SE401'), ('T17', 'SE501'),
    ('T18', 'CS101'), ('T18', 'SE201'), ('T18', 'SE501'), ('T18', 'DB301');

-- Math / Stats teachers
INSERT INTO teacher_subjects (teacher_id, subject_code) VALUES
    ('T03', 'MATH101'), ('T03', 'MATH201'), ('T03', 'STAT301'),
    ('T11', 'MATH101'), ('T11', 'MATH201'), ('T11', 'MATH301'), ('T11', 'STAT301'),
    ('T19', 'MATH301'), ('T19', 'MATH401'), ('T19', 'STAT301'),
    ('T20', 'MATH101'), ('T20', 'MATH201'), ('T20', 'MATH401'),
    ('T21', 'STAT301'), ('T21', 'MATH301'), ('T21', 'MATH401'), ('T21', 'MATH201');

-- Physics teachers
INSERT INTO teacher_subjects (teacher_id, subject_code) VALUES
    ('T04', 'PHY101'), ('T04', 'PHY201'), ('T04', 'EE201'),
    ('T22', 'PHY101'), ('T22', 'PHY201'), ('T22', 'PHY301'),
    ('T23', 'PHY101'), ('T23', 'PHY201'), ('T23', 'PHY301');

-- EE teachers
INSERT INTO teacher_subjects (teacher_id, subject_code) VALUES
    ('T05', 'EE101'), ('T05', 'EE201'), ('T05', 'EE301'), ('T05', 'EE401'),
    ('T24', 'EE301'), ('T24', 'EE401'), ('T24', 'EE501'), ('T24', 'EE601'),
    ('T25', 'EE101'), ('T25', 'EE201'), ('T25', 'EE501'), ('T25', 'EE601'),
    ('T26', 'EE401'), ('T26', 'EE501'), ('T26', 'EE601'), ('T26', 'PHY301');

-- Business / Management teachers
INSERT INTO teacher_subjects (teacher_id, subject_code) VALUES
    ('T06', 'BUS101'), ('T06', 'BUS201'), ('T06', 'MGT301'), ('T06', 'MGT401'),
    ('T10', 'MGT201'), ('T10', 'MGT301'), ('T10', 'BUS301'), ('T10', 'BUS401'),
    ('T27', 'FIN301'), ('T27', 'FIN401'), ('T27', 'BUS401'), ('T27', 'BUS501'),
    ('T28', 'BUS101'), ('T28', 'BUS201'), ('T28', 'BUS501'), ('T28', 'MGT201'),
    ('T29', 'MGT301'), ('T29', 'MGT401'), ('T29', 'FIN301'), ('T29', 'FIN401'),
    ('T30', 'BUS301'), ('T30', 'BUS401'), ('T30', 'BUS501'), ('T30', 'FIN301');

-- English / Humanities / General teachers
INSERT INTO teacher_subjects (teacher_id, subject_code) VALUES
    ('T07', 'ENG101'), ('T07', 'ENG201'), ('T07', 'HUM301'),
    ('T12', 'ENG101'), ('T12', 'ENG201'), ('T12', 'HUM201'), ('T12', 'HUM301'),
    ('T31', 'ENG101'), ('T31', 'ENG201'), ('T31', 'ISL101'),
    ('T32', 'HUM201'), ('T32', 'HUM301'), ('T32', 'ISL101'), ('T32', 'ENG101'),
    ('T33', 'ISL101'), ('T33', 'HUM201'), ('T33', 'HUM301'),
    ('T34', 'ENG101'), ('T34', 'ENG201'), ('T34', 'HUM201'), ('T34', 'ISL101'),
    ('T35', 'ENG101'), ('T35', 'ENG201'), ('T35', 'HUM301'), ('T35', 'ISL101'),
    ('T36', 'ENG201'), ('T36', 'HUM201'), ('T36', 'HUM301'), ('T36', 'ISL101'),
    ('T37', 'DB301'),  ('T37', 'CS201'),  ('T37', 'CS501'),  ('T37', 'SE301'),
    ('T38', 'STAT301'),('T38', 'MATH201'),('T38', 'MATH301'),('T38', 'HUM201');

-- ── Batch ↔ Subject mappings ───────────────────────────────────────────────
-- CS batches
INSERT INTO batch_subjects (batch, subject_code) VALUES
    ('CS-1A', 'CS101'), ('CS-1A', 'MATH101'), ('CS-1A', 'PHY101'), ('CS-1A', 'ENG101'), ('CS-1A', 'ISL101'), ('CS-1A', 'SE201'),
    ('CS-2A', 'CS201'), ('CS-2A', 'MATH201'), ('CS-2A', 'ENG201'), ('CS-2A', 'DB301'),  ('CS-2A', 'CS501'),  ('CS-2A', 'HUM201'),
    ('CS-3A', 'CS301'), ('CS-3A', 'CS401'),   ('CS-3A', 'SE401'),  ('CS-3A', 'STAT301'),('CS-3A', 'AI401'),  ('CS-3A', 'HUM301'),
    ('CS-4A', 'AI401'), ('CS-4A', 'ML401'),   ('CS-4A', 'HUM301'), ('CS-4A', 'DB301'),  ('CS-4A', 'SE501'),  ('CS-4A', 'MATH401');

-- SE batches
INSERT INTO batch_subjects (batch, subject_code) VALUES
    ('SE-1A', 'CS101'), ('SE-1A', 'MATH101'), ('SE-1A', 'ENG101'), ('SE-1A', 'SE201'), ('SE-1A', 'ISL101'), ('SE-1A', 'PHY101'),
    ('SE-2A', 'CS201'), ('SE-2A', 'SE301'),   ('SE-2A', 'DB301'),  ('SE-2A', 'ENG201'),('SE-2A', 'MATH201'),('SE-2A', 'HUM201'),
    ('SE-3A', 'CS301'), ('SE-3A', 'SE401'),   ('SE-3A', 'HUM201'), ('SE-3A', 'STAT301'),('SE-3A', 'AI401'), ('SE-3A', 'MATH301'),
    ('SE-4A', 'AI401'), ('SE-4A', 'SE401'),   ('SE-4A', 'MGT301'), ('SE-4A', 'CS401'), ('SE-4A', 'ML401'),  ('SE-4A', 'HUM301');

-- EE batches
INSERT INTO batch_subjects (batch, subject_code) VALUES
    ('EE-1A', 'EE101'), ('EE-1A', 'MATH101'), ('EE-1A', 'PHY101'), ('EE-1A', 'ENG101'), ('EE-1A', 'ISL101'), ('EE-1A', 'EE601'),
    ('EE-2A', 'EE201'), ('EE-2A', 'MATH201'), ('EE-2A', 'PHY201'), ('EE-2A', 'ENG201'), ('EE-2A', 'EE501'),  ('EE-2A', 'HUM201'),
    ('EE-3A', 'EE301'), ('EE-3A', 'EE401'),   ('EE-3A', 'STAT301'),('EE-3A', 'HUM201'), ('EE-3A', 'MATH301'),('EE-3A', 'EE501'),
    ('EE-4A', 'EE401'), ('EE-4A', 'MATH301'), ('EE-4A', 'MGT401'), ('EE-4A', 'HUM301'), ('EE-4A', 'EE601'),  ('EE-4A', 'PHY301');

-- BBA batches
INSERT INTO batch_subjects (batch, subject_code) VALUES
    ('BBA-1A', 'BUS101'), ('BBA-1A', 'MATH101'),('BBA-1A', 'ENG101'),('BBA-1A', 'MGT201'),('BBA-1A', 'ISL101'),('BBA-1A', 'HUM201'),
    ('BBA-2A', 'BUS201'), ('BBA-2A', 'BUS301'), ('BBA-2A', 'ENG201'),('BBA-2A', 'MGT301'),('BBA-2A', 'FIN301'),('BBA-2A', 'HUM301'),
    ('BBA-3A', 'BUS401'), ('BBA-3A', 'MGT301'), ('BBA-3A', 'HUM201'),('BBA-3A', 'STAT301'),('BBA-3A', 'FIN401'),('BBA-3A', 'BUS501'),
    ('BBA-4A', 'MGT201'), ('BBA-4A', 'MGT401'), ('BBA-4A', 'HUM301'),('BBA-4A', 'BUS301'),('BBA-4A', 'FIN301'),('BBA-4A', 'ISL101');

-- ============================================================================
-- VERIFY
-- ============================================================================
SELECT 'teachers' AS "table", COUNT(*) AS rows FROM teachers
UNION ALL SELECT 'subjects',         COUNT(*) FROM subjects
UNION ALL SELECT 'departments',      COUNT(*) FROM departments
UNION ALL SELECT 'batches',          COUNT(*) FROM batches
UNION ALL SELECT 'teacher_subjects', COUNT(*) FROM teacher_subjects
UNION ALL SELECT 'batch_subjects',   COUNT(*) FROM batch_subjects;
