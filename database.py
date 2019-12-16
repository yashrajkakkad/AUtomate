import sqlite3

conn = sqlite3.connect('db.sqlite3', isolation_level=None)
c = conn.cursor()

try:
    c.execute("""CREATE TABLE tbl_attendance (
        course_code PRIMARY KEY references tbl_course(code),
        present integer,
        absent integer
        )""")
except sqlite3.OperationalError:
    pass

try:
    c.execute("""CREATE TABLE tbl_components (
        name text,
        marks_obt integer,
        marks_outof integer,
        marks_verifyby text,
        course_code references course(code)
    )
    """)
except sqlite3.OperationalError:
    pass

try:
    c.execute("""CREATE TABLE tbl_courses (
        code text PRIMARY KEY NOT NULL,
        name text NOT NULL
    )
    """)
except sqlite3.OperationalError:
    pass

print("Your database is set!")

conn.close()
