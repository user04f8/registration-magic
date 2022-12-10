import time

from courses import Semester

URL_BASE = 'https://www.bu.edu/link/bin/uiscgi_studentlink.pl/'

def url_generator(s : Semester, planner = False) -> str:        
    for course in s.course_iter():
        yield URL_BASE + str(int(time.time())) + s.getURLparams(course, planner=planner)