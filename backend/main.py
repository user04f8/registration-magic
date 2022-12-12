import requests
#import threading
#import time
from datetime import datetime
import asyncio
import json

#import schedule
import flask

from courses import Semester, Course
from coursedb import CourseDB
from user import User
from utils import url_generator, preprocess_user_input

COURSE_DATABASE_FILENAME = 'Course_Info.xlsx'
SCHEDULED_EVENTS_INTERVAL = 1 # seconds per checking scheduled events
DEFAULT_TIME = datetime(2022, 12, 11, 20, 0, 0)

#async def wait_until(dt):
#    await asyncio.sleep((dt - datetime.datetime.now()).total_seconds())

async def run_at(dt, method):
    await asyncio.sleep((dt - datetime.now()).total_seconds()) # requires python version 3.8 or above
    return await method

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
user.set_active_semester('Spring', 2022)
loop = asyncio.new_event_loop() # initialize an event loop to schedule registration at specific times


@app.route('/', methods=['GET', 'POST'])
def default_output():
    print(flask.request.get_json())
    print(flask.request.json)
    response = {'query': 'hello_world'}
    return flask.jsonify(response)

@app.route('/request', methods=['POST'])
def schedule_registration() -> flask.Response: # bind the Flask input to this method
    data = flask.request.json #json.loads(flask.request.json)
    # data = {'classList': '[["CAS MA225 B2"]]', 'time': '12/11/2022 9:00 PM'}
    print(data)
    time_raw = data['time']
    courses = json.loads(data['classList'])
    try:
        scheduled_time = datetime.strptime(time_raw, r'%d/%m/%Y %I:%M %p') # dd/mm/yyyy hh:mm [AM/PM]
    except:
        print(f"Warning: defaulting to time {DEFAULT_TIME}")
        scheduled_time = DEFAULT_TIME # default time to avoid errors
    print(f"Scheduling courses {courses} at {scheduled_time}")
    for course in courses:
        print(course)
        user.add_course(Course(coursedb, *preprocess_user_input(course[0])))
    loop.create_task(run_at(scheduled_time, register(user)))

    json_file = {}
    #json_file['query'] = 'sample response'
    return flask.jsonify(json_file)


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=53303)

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
