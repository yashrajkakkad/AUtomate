import re
import datetime
import sqlite3


class Component:
    def __init__(self, name, marks_obt, marks_outof, course_code, verify_by):
        self.name = name
        self.marks_obt = marks_obt
        self.marks_outof = marks_outof
        self.verify_by = verify_by
        # self.verify_by = datetime.date(datetime.MINYEAR, 1, 1)
        self.course_code = course_code

    def tuple(self):
        return self.name, self.marks_obt, self.marks_outof, self.verify_by, self.course_code

    @staticmethod
    def extract_components(raw_data, course_code):
        # component_regex = re.compile(
        #     r'.*Evaluation Type: (\S+) Marks: (\d+)-(\d+) Apply for verification of marks / grades by (\d{2})-(\d{2})-(\d{4})(.*)')
        # component_regex = re.compile(
        #     r'.*?Evaluation Type: ([a-zA-Z\[\]0-9].*?) Marks: (\d+)/(\d+) Apply for verification of marks / grades by (\d{2})-(\d{2})-(\d{4})')
        component_regex = re.compile(
            r'.*?Evaluation Type: ([a-zA-Z\[\]0-9].*?)\sMarks: (\d+)(\.\d)?/(\d+)(\s)?(Apply for verification of marks / grades by (\d{2})-(\d{2})-(\d{4}))?')
        matches = component_regex.findall(raw_data)
        components = []
        for match in matches:
            name = match[0]
            marks_obt = int(match[1])
            marks_outof = int(match[3])
            # print(name)
            # print(match[5])
            # verify_regex = re.compile(
            #     r'Apply for verification of marks / grades by \d{2}-\d{2}-\d{4}')
            # date_search = verify_regex.search(match[4])
            verify_by = datetime.date(datetime.MINYEAR, 1, 1)
            if match[5] != "":
                # print(match[6], match[7], match[8])
                verify_by = datetime.date(
                    int(match[8]), int(match[7]), int(match[6]))
            # if date_search is not None:
            #     # print("Chill bro")
            #     verify_by = datetime.date(reversed(date_search.group()))
            component = Component(
                name, marks_obt, marks_outof, course_code, verify_by)
            components.append(component)
            # print(name)
        return components

    @staticmethod
    def insert_component(component):
        # First check if the component already exists. If it does, check if data is updated
        select_query = 'SELECT marks_obt FROM tbl_components WHERE name = ? AND course_code = ?'
        insert_query = 'INSERT INTO tbl_components VALUES(?,?,?,?,?)'
        update_query = 'UPDATE tbl_components SET marks_obt = ? WHERE name = ? AND course_code = ?'
        conn = None
        try:
            conn = sqlite3.connect('db.sqlite3', isolation_level=None)
        except:
            print("Well, are you sure you're connected to internet?")
            return
        c = conn.cursor()
        c.execute(select_query, (component.name, component.course_code))
        marks_obt = c.fetchone()
        # print(component.name)
        # print('Detected marks:', component.marks_obt)
        if marks_obt is None:
            print("New score alert! You've got {} out of {} in {} - {}".format(
                component.marks_obt, component.marks_outof, component.course_code, component.name))
            c.execute(insert_query, component.tuple())
        elif marks_obt[0] != int(component.marks_obt):
            print("Your score in {} for component {} has been updated to {}/{}".format(
                component.course_code, component.name, component.marks_obt, component.marks_outof))
            c.execute(update_query, (component.marks_obt,
                                     component.name, component.course_code))
        conn.close()

# raw_data = "Evaluation Type: encyclopedic article [encyclopedic article] Marks: 19/20 Apply for verification of marks / grades by 05-12-2018Evaluation Type: Opinion Piece [Opinion Piece] Marks: 17/20 Your marks / grades have been verifiedEvaluation Type: Literature Review [Literature Review] Marks: 18/20 Apply for verification of marks / grades by 05-12-2018Evaluation Type: Educational Video [Educational Video] Marks: 19/20 Apply for verification of marks / grades by 05-12-2018Evaluation Type: Class participation (Including attendance) [Class Participation] Marks: 18/20 Apply for verification of marks / grades by 05-12-2018"
# components = extract_components(raw_data)
# for component in components:
#     print(component.name)
