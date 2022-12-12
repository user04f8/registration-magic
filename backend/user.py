import requests
import time

from courses import Semester, Course
from coursedb import CourseDB
from utils import url_generator

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

    def register(self):
        if self.active_sem_id is not None:
            active_semester : Semester = self.sems[self.active_sem_id]
        else:
            raise Exception('No active semester id set, use set_active_semester() first')

        for url in url_generator(active_semester, planner=False):
            print(url)
            response = requests.post(url) 
            # TODO
            # probably the easiest most user-friendly means is to show this URL in the frontend
            print(response)
            print(response.text)
            time.sleep(0.1)
    
    """
    def add_course_to_semester(self, course : Course, semester : str, year : int):
        id = Semester.getid(semester, year)
        if id in self.sems:
            self.sems[id].add_course(course)
        else:
            self.sems[id] = Semester(semester, year).add_course(course)
    """

    