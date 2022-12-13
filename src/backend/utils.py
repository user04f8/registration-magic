import time

from courses import Course, Semester

URL_BASE = 'https://www.bu.edu/link/bin/uiscgi_studentlink.pl/'

def url_generator(s : Semester, planner = False) -> str:        
    for course in s.course_iter():
        yield URL_BASE + str(int(time.time())) + s.getURLparams(course, planner=planner)

def get_auth_url() -> str:
    return URL_BASE + str(int(time.time())) + '?ModuleName=regsched.pl'

def preprocess_user_input(user_input : str) -> tuple:
    """
    takes in user input in the following format, removing whitespace: 'ENGEC327A1'
    returns: tuple[str, str, int(, str)] (arguments for creating a Course() object)
    """
    user_input = "".join(user_input.split()) # remove all whitespace
    #Assume user_input is valid (has already been validated on the frontend)
    if (len(user_input) == 8):
        return (user_input[0:3], user_input[3:5], int(user_input[5:8]))
    elif (len(user_input) == 10):
        return (user_input[0:3], user_input[3:5], int(user_input[5:8]), user_input[8:10])
    else:
        raise Exception(f'Invalid user input {user_input}\nshould be len == 8 (no section) or len == 8, got len == {len(user_input)}')
