import component
import sqlite3


class Course:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.components = []

    def add_component(self, component: component):
        components.append(component)

    @staticmethod
    def insert_course(course):
        insert_query = 'INSERT INTO tbl_courses(code, name) VALUES(?,?)'
        try:
            conn = sqlite3.connect('db.sqlite3', isolation_level=None)
        except:
            print("Not able to connect to database")
            return
        c = conn.cursor()
        try:
            c.execute(insert_query, (course.code, course.name))
            print("New course added!", course.code, course.name)
        except sqlite3.IntegrityError:
            pass
        conn.close()
