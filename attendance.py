import sqlite3
import re
from course import Course


class Attendance:

    def __init__(self, course_code, present, absent):
        self.course_code = course_code
        self.present = present
        self.absent = absent

    def tuple(self):
        return self.course_code, self.present, self.absent

    @staticmethod
    def insert_attendance(raw_data):
        attendance_regex_old = re.compile(
            r'([a-zA-Z0-9]+?) ([a-zA-Z0-9 ]+?)\nSection \d\n\d{2}-[A-Za-z]{3}-\d{4}\n\d+\s+(\d+)\s+(\d+)')
        matches = attendance_regex_old.findall(raw_data)
        for match in matches:
            Course.insert_course(Course(match[0], match[1]))
            attendance_obj = Attendance(match[0], match[2], match[3])
            # print("Match: ", match)
            Attendance.update_attendance(attendance_obj)
        attendance_regex_new = re.compile(
            r'([a-zA-Z0-9]+?) ([a-zA-Z0-9 ]+?)\nSection \d\n\d{2}-[A-Za-z]{3}-\d{4} \d{2}:\d{2}\n\d+\s+(\d+)\s+(\d+)')
        matches = attendance_regex_new.findall(raw_data)
        for match in matches:
            Course.insert_course(Course(match[0], match[1]))
            attendance_obj = Attendance(match[0], match[2], match[3])
            # print("Match: ", match)
            Attendance.update_attendance(attendance_obj)

    @staticmethod
    def update_attendance(attendance):
        select_query = 'SELECT present, absent FROM tbl_attendance WHERE course_code = ?'
        insert_query = 'INSERT INTO tbl_attendance VALUES(?,?,?)'
        update_query = 'UPDATE tbl_attendance SET present = ?, absent = ? WHERE course_code = ?'
        try:
            conn = sqlite3.connect('db.sqlite3', isolation_level=None)
        except:
            print("Well, are you sure you're connected to database?")
            return
        # First check if course is added or not - run insert_course
        c = conn.cursor()
        c.execute(select_query, (attendance.course_code,))
        try:
            row = c.fetchone()
            present, absent = row
            print(attendance.course_code, present, absent,
                  attendance.present, attendance.absent)
            if present != int(attendance.present) or absent != int(attendance.absent):
                c.execute(update_query, (attendance.present,
                                         attendance.absent, attendance.course_code))
                print("Attendance in {} updated to {}/{}".format(
                    attendance.course_code, attendance.present, attendance.absent))
        except (ValueError, TypeError):
            c.execute(insert_query, attendance.tuple())
            print("New subject alert : {} - {}/{}".format(
                attendance.course_code, attendance.present, attendance.absent))
        conn.close()
