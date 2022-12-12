import requests
#import threading
#import time
import datetime
import asyncio

#import schedule
import flask

from courses import Semester, Course
from coursedb import CourseDB
from user import User
from utils import url_generator, preprocess_user_input

COURSE_DATABASE_FILENAME = 'Course_Info.xlsx'
SCHEDULED_EVENTS_INTERVAL = 1 # seconds per checking scheduled events

#async def wait_until(dt):
#    await asyncio.sleep((dt - datetime.datetime.now()).total_seconds())

async def wait_until(dt):
    # sleep until the specified datetime
    now = datetime.datetime.now()
    await asyncio.sleep((dt - now).total_seconds())

async def run_at(dt, coro):
    await wait_until(dt)
    return await coro

# https://stackoverflow.com/questions/51292027/how-to-schedule-a-task-in-asyncio-so-it-runs-at-a-certain-date

"""
async def run_at(dt, method):
    await asyncio.sleep((dt - datetime.datetime.now()).total_seconds()) # requires python version 3.8 or above
    return await method
    """

async def register(user : User):
    user.register() # runs the register() method on the user exactly once 

"""
def run_scheduled_actions(interval):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run
"""

app = flask.Flask(__name__) # initialize the Flask app
coursedb = CourseDB(COURSE_DATABASE_FILENAME) # initialize the database
user = User(coursedb) # initialize a default user for now
loop = asyncio.get_event_loop() # initialize an event loop to schedule registration at specific times

@app.route('/')
def schedule_registration(courses, timestr : str) -> flask.Response: # bind the Flask input to this method
    scheduled_time = datetime.strptime(timestr, r'%d/%m/%Y-%H:%M:%S.%f')
    
    for course in courses:
        user.add_course(Course(coursedb, *preprocess_user_input(course)))    
    loop.create_task(run_at(scheduled_time, register(user)))

    json_file = {}
    #json_file['query'] = 'sample response'
    return flask.jsonify(json_file)

if __name__ == '__main__':

    app.run()
    
    """
    print('Flask stopped, press q then enter to close remaining threads...')
    inpt = ''
    while (inpt != 'q'):
        inpt = input()
        print('Press q then enter to close remaining threads...')
    stop_event.set()
    """

"""
#TODO add handling for multiple users?
users : dict(User) = {}
@app.route('/')
def add_user(username : str):
    users[username] = User(coursedb)
"""

if __name__ == '__main__':
    app.run()
