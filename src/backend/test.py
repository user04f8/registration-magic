from courses import Semester, Course
from coursedb import CourseDB
from user import User
from utils import url_generator, preprocess_user_input

COURSE_DATABASE_FILENAME = 'Course_Info.xlsx'
SCHEDULED_EVENTS_INTERVAL = 1 # seconds per checking scheduled events

def test_register():
    coursedb = CourseDB(COURSE_DATABASE_FILENAME)
    user = User(coursedb)
    user.set_active_semester('Spring', 2023)
    user.add_course(Course(coursedb, 'CAS', 'AA', 112))
    user.register()

def test_flask():

    # py main.py &
    import requests
    response = requests.put('http://127.0.0.1:5000', {
        'test': 'object'
    })
    print(response, response.text)

if __name__ == '__main__':
    test_flask()