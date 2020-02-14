from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup as bs
from decouple import config
import re
from course import Course
from component import Component
from attendance import Attendance
import os

EMAIL = config('EMAIL')
PASSWORD = config('PASSWORD')

driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"))
driver.get('http://auris.ahduni.edu.in')

# Press "Sign in with Google"
sign_in = driver.find_element_by_xpath("// *[contains(@id, 'not_signed_in')]")
sign_in.click()

# "Switch to pop-up window"
main_window = driver.window_handles[0]
oauth_window = driver.window_handles[1]
driver.switch_to.window(oauth_window)

# time.sleep(7)

# "Enter email"
identifier_id = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'identifierId')))
time.sleep(1)
# identifier_id = driver.find_element_by_id('identifierId')
identifier_id.send_keys(EMAIL)
identifier_id.send_keys(Keys.RETURN)
time.sleep(2)

# "Enter password"
password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@aria-label=\'Enter your password\']')))
# password = driver.find_element_by_xpath(
#     "//input[@aria-label='Enter your password']")
password.send_keys(PASSWORD)
password.send_keys(Keys.RETURN)
time.sleep(12)

# "Switch to Scores Window. Scrape!"
driver.switch_to.window(main_window)
# temp_element = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CLASS_NAME, 'logo')))
print("\nFetching attendance")
driver.get('https://auris.ahduni.edu.in/core-emli/code/student_portal/home.php?page=quick_link/attendence')
attendance_html = driver.page_source

# attendance_html = open('attendance.html')
attendance_soup = bs(attendance_html, 'lxml')
tables = attendance_soup.find_all('table')
for table in tables:
    table_rows = table.find_all('tr')
    for i, tr in enumerate(table_rows):
        # if i == 0:
        #     continue
        td_rs = tr.find_all('td')
        # print(td_rs)
        raw_list = []
        # print("New result-set: ")
        for td in td_rs:
            raw_list.append(td.text)
        raw_data = '\n'.join(raw_list)
        # print(raw_data)
        Attendance.insert_attendance(raw_data)

print("\nFetching scores")
driver.get('https://auris.ahduni.edu.in/core-emli/code/student_portal/home.php?page=notification/exam_result')
temp_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'logo')))
# # time.sleep(10)
scores_html = driver.page_source
# scores_html = open('test.html')
scores_soup = bs(scores_html, 'lxml')

tables = scores_soup.find_all('table')
# print(type(tables))
newlineRegex = re.compile(r'\s*<br/>\s*')
horizontalRegex = re.compile(r'\s*<hr/>\s*')

for table in tables:
    table_rows = table.find_all('tr')
    # print("Table: ")
    for tr in table_rows:
        # print("Row: ")
        td_rs = tr.find_all('td')
        current_ccode = None

        for i in range(len(td_rs)):
            td = newlineRegex.sub('\n', td_rs[i].__str__())
            td = horizontalRegex.sub('\n', td)
            soup = bs(td, 'lxml')
            td = soup.text
            # print(td)
            if i == 0:
                if td != '':
                    keywords = td.split()
                    course_code = keywords[0]
                    course_name = ' '.join(keywords[1:])
                    # print(course_code, course_name)
                    course = Course(course_code, course_name)
                    current_ccode = course_code
                    Course.insert_course(course)
            else:
                components = Component.extract_components(td, current_ccode)
                for component in components:
                    # print(component.verify_by)
                    # print(component.marks_obt)
                    Component.insert_component(component)

# abscence_html = driver.page_source
# abscence_soup = bs(abscence_html, 'lxml')
# absence_tags = abscence_soup.find_all('div', color='red')
# left_button = driver.find_element_by_class_name('fc-icon-left-single-arrow')
