import requests
import time

from courses import Semester, Course
from coursedb import CourseDB
from user import User
from utils import url_generator, preprocess_user_input

from flask import Flask
import flask

COURSE_DATABASE_FILENAME = 'Course_Info.xlsx'

def test_project():

    coursedb = CourseDB(COURSE_DATABASE_FILENAME)
    user = User(coursedb)
    user.set_active_semester('Spring', 2023)
    user.add_course(Course(coursedb, 'CAS', 'AA', 112))
    
    user.register()

coursedb = CourseDB(COURSE_DATABASE_FILENAME)
user = User(coursedb)

app = Flask(__name__)

@app.route('/')
def schedule_registration(courses : list(str) , timestr : str) -> flask.Response:
    time.strptime(timestr, '%d/%m/%Y-%H:%M:%S.%f')
    
    for course in courses:
        user.add_course(Course(coursedb, *preprocess_user_input(course)))

    json_file = {}
    json_file['query'] = 'hello_world'
    return flask.jsonify(json_file) 




if __name__ == '__main__':
    app.run()

""" #TODO add handling for multiple users?
users : dict(User) = {}
@app.route('/')
def add_user(username : str):
    users[username] = User(coursedb)
"""


    


if __name__ == '__main__':
    app.run()
