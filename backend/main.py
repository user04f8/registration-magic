import requests
import time

from courses import Semester, Course


def main():
    URL = 'https://www.bu.edu/link/bin/uiscgi_studentlink.pl/'
    s = Semester('Spring', 2023)
    c = Course('ENG', 'EC', 327, 'A1')
    url = URL + str(int(time.time())) + s.getURLparams(c)
    
    print(requests.post(url).json)

    list_of_courses : list
    selectit_dict : dict

    #psuedocode for web scraper
    #for course in list_of_courses:
    #    response = requests.post(URL + str(int(time.time())) + s.getURLparams(course)).json
    #    selectit : int = ...
    #    write directly to a csv file OR selectit_dict[course] = selectit
    #    time.sleep(0.1)


    #print('Initializing backend...')
    #TODO: run some sort of python server e.g. Django to handle requests from the frontend

    








if __name__ == '__main__':
    main()