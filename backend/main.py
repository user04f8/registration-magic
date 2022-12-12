import requests
#import threading
#import time
from datetime import datetime
from time import sleep
import asyncio
import threading
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
DEFAULT_SEMESTER = ('Spring', 2023)

async def run_at(dt, method):
    await asyncio.sleep((dt - datetime.now()).total_seconds()) # requires python version 3.8 or above
    return await method

async def register(user : User):
    print('Performing course registration for user {user.id}:')
    user.register() # runs the register() method on the user exactly once 

app = flask.Flask(__name__) # initialize the Flask app
coursedb = CourseDB(COURSE_DATABASE_FILENAME) # initialize the database
user = User(coursedb) # initialize a default user for now
user.set_active_semester(*DEFAULT_SEMESTER)
user.prep_auth() # capture the user's auth token by having them sign in to the student link
loop = asyncio.new_event_loop() # initialize an event loop to schedule registration at specific times

def run_app():
    app.run(host='127.0.0.1', port=53303)

def run_loop():
    loop.run_forever()

@app.route('/', methods=['GET', 'POST'])
def default_output():
    print(flask.request.get_json())
    print(flask.request.json)
    response = {'status': 'Flask server online'}
    return flask.jsonify(response)

@app.route('/request', methods=['POST'])
def api_request_handler() -> flask.Response: # bind the Flask input to this method
    data = flask.request.json
    schedule_registration(data)
    json_file = {}
    #json_file['query'] = 'response'
    return flask.jsonify(json_file)

def schedule_registration(data : str):
    print(data)
    scheduled_time = 'now'
    if 'time' not in data:
        time_raw = 'NOW'
    else:
        time_raw = data['time']
    courses = json.loads(data['classList'])
    plan = 'plan' in data
    if time_raw != 'NOW':
        try:
            scheduled_time = datetime.strptime(time_raw, r'%d/%m/%Y %I:%M %p') # dd/mm/yyyy hh:mm [AM/PM]
        except:
            print(f"Warning: defaulting to time {DEFAULT_TIME}")
            scheduled_time = DEFAULT_TIME # default time to avoid errors
    print(f"Scheduling courses {courses} at {scheduled_time}")
    for course in courses:
        user.add_course(Course(coursedb, *preprocess_user_input(course[0])))
    if time_raw != 'NOW':
        sleeptime : int = (scheduled_time - datetime.now()).seconds + 86400 * (scheduled_time - datetime.now()).days
        print(f'Waiting {sleeptime} seconds. . .')
        sleep(sleeptime)
    user.register()
    #loop.create_task(run_at(scheduled_time, register(user)))    

def test_scheduler():
    schedule_registration(data = {'classList': '[["CAS AA385 A1"]]', 'time': 'NOW'})

#https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1670822671?SelectIt=0001151409&ModuleName=reg%2Fadd%2Fconfirm_classes.pl&AddPreregInd=&AddPlannerInd=&ViewSem=Spring+2023&KeySem=20234&PreregViewSem=&PreregKeySem=&SearchOptionCd=S&SearchOptionDesc=Class+Number&MainCampusInd=&BrowseContinueInd=&ShoppingCartInd=&ShoppingCartList=
#https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1670822639?SelectIt=0001151409&ModuleName=reg%2Fadd%2Fconfirm_classes.pl&AddPreregInd=&AddPlannerInd=&ViewSem=Spring+2023&KeySem=20234&PreregViewSem=&PreregKeySem=&SearchOptionCd=S&SearchOptionDesc=Class+Number&MainCampusInd=&BrowseContinueInd=&ShoppingCartInd=&ShoppingCartList=

#https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1670820688?SelectIt=0001151409&ModuleName=reg%2Fadd%2Fconfirm_classes.pl&AddPreregInd=&AddPlannerInd=&ViewSem=Spring+2023&KeySem=20234&PreregViewSem=&PreregKeySem=&SearchOptionCd=S&SearchOptionDesc=Class+Number&MainCampusInd=&BrowseContinueInd=&ShoppingCartInd=&ShoppingCartList=
#https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1670820707?SelectIt=0001151409&College=CAS&Dept=AA&Course=385&Section=A1&ModuleName=reg%2Fadd%2Fconfirm_classes.pl&AddPreregInd=&AddPlannerInd=&ViewSem=Spring+2022&KeySem=20223&PreregViewSem=&PreregKeySem=&SearchOptionCd=S&SearchOptionDesc=Class+Number&MainCampusInd=&BrowseContinueInd=&ShoppingCartInd=&ShoppingCartList=

#https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1670820688?SelectIt=0001151409&ModuleName=reg%2Fadd%2Fconfirm_classes.pl&AddPreregInd=&AddPlannerInd=&ViewSem=Spring+2023&KeySem=20234&PreregViewSem=&PreregKeySem=&SearchOptionCd=S&SearchOptionDesc=Class+Number&MainCampusInd=&BrowseContinueInd=&ShoppingCartInd=&ShoppingCartList=
#https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1670820825?SelectIt=0001151409&ModuleName=reg%2Fadd%2Fconfirm_classes.pl&AddPreregInd=&AddPlannerInd=&ViewSem=Spring+2022&KeySem=20223&PreregViewSem=&PreregKeySem=&SearchOptionCd=S&SearchOptionDesc=Class+Number&MainCampusInd=&BrowseContinueInd=&ShoppingCartInd=&ShoppingCartList=

if __name__ == '__main__':
    test_scheduler()
    loop_thread = threading.Thread(target=run_loop)
    loop_thread.start()
    print('Asyncio initialization complete')
    app_thread = threading.Thread(target=run_app)
    app_thread.start()
    app_thread.join()
    print('Flask app forcibly stopped; stopping loop')
    loop.stop()
    print('Press CTRL+C to close remaining threads')
    sleep(1)
    exit()
    while True: 
        sleep(1) #catch ctrl + c if exit() fails somehow
            
    

"""
users : dict(User) = {}
@app.route('/adduser')
def add_user(username : str):
    users[username] = User(coursedb)
"""
