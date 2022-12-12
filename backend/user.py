import requests
import time
import webbrowser

from courses import Semester, Course
from coursedb import CourseDB
from utils import url_generator, get_auth_url

class User:
    def __init__(self, coursedb : CourseDB, id=0):
        self.coursedb = coursedb
        self.active_sem_id = None
        self.sems = {}
        self.schedule_time = None
        self.id = id

    def set_active_semester(self, semester : str, year : int):
        self.active_sem_id = Semester.getid(semester, year)
        if self.active_sem_id not in self.sems:
            self.sems[self.active_sem_id] = Semester(semester, year)

    def add_course(self, course : Course):
        if self.active_sem_id is not None:
            self.sems[self.active_sem_id].add_course(course)
            print(f"Course {course} successfully added!")
        else:
            raise Exception('No active semester id set, use set_active_semester() first')

    # (TODO: validate auth before registration)
    # 
    # TODO: set a scheduler for this registration to occur at the requested time

    @staticmethod
    def prep_auth():
        webbrowser.open(get_auth_url())

    def register(self):
        if self.active_sem_id is not None:
            active_semester : Semester = self.sems[self.active_sem_id]
        else:
            raise Exception('No active semester id set, use set_active_semester() first')

        i = 0
        for url in url_generator(active_semester, planner=False):
            print(url)
            webbrowser.open(url) # for locally hosted backend

            #response = requests.post(url)
            # this method only works if the auth token has already been captured -- more user friendly to just use webbrowser instead
            # of dealing with potential security issues with storing user's BU authentication and issues if auth token expires
            # before registration starts
            #print(response)
            #print(response.text)            
            if (i > 20):
                time.sleep(0.1) # rate limit so we don't ddos student link
            i += 1
    
    """
    def add_course_to_semester(self, course : Course, semester : str, year : int):
        id = Semester.getid(semester, year)
        if id in self.sems:
            self.sems[id].add_course(course)
        else:
            self.sems[id] = Semester(semester, year).add_course(course)
    """

    