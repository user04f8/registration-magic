import requests
import time

from courses import Semester, Course
from coursedb import CourseDB
from utils import url_generator

COURSE_DATABASE_FILENAME = 'Course_Info.xlsx'

def main():

    coursedb = CourseDB(COURSE_DATABASE_FILENAME)
    
    s = Semester('Spring', 2023)
    s.add_course(Course(coursedb, 'CAS', 'AA', 112))
    #s.add_course(Course(coursedb, 'ENG', 'EC', 327, 'A1'))
    for url in url_generator(s, planner=False):
        print(url)
        exit()
        response = requests.post(url)
        print(response)
        print(response.text)
        time.sleep(0.01)

    

    #psuedocode for web scraper
    """
    s = Semester('Spring', 2023)
    course = Course('CAS','AA','111','A1')
    while not stop:
        response = requests.post(s.getURL(course))
        for idx in FIND EVERY SUBSTRING OF 'value=' IN response.text
            selectit : int = int( response.text[idx+7:idx+17] SOME OFFSET OF THAT SUBSTRING )
            course_code : str = SOME OFFSET OF THE INDEX POINTING TO THAT SUBSTRING
            write directly to a csv file
            if (ARE WE AT THE LAST 4 INSTANCES OF VALUE):
                break
        course_info = VALUES AT LAST 4 INSTANCES OF value="..."
        course = Course(*course_info)
        time.sleep(0.1)
    """

    #print('Initializing backend...')
    #TODO: run some sort of python server e.g. Django to handle requests from the frontend

    








if __name__ == '__main__':
    main()