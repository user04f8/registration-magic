import requests
import time

from courses import Semester, Course
from coursedb import CourseDB
from user import User
from utils import url_generator

COURSE_DATABASE_FILENAME = 'Course_Info.xlsx'

def main():

    coursedb = CourseDB(COURSE_DATABASE_FILENAME)
    user = User(coursedb)
    user.set_active_semester('Spring', 2023)
    user.add_course(Course(coursedb, 'CAS', 'AA', 112))
    #user.add_course(Course(coursedb, 'ENG', 'EC', 327, 'A1'))
    
    user.register()
    
    #TODO: run some sort of python server e.g. Django to handle requests from the frontend

    








if __name__ == '__main__':
    main()