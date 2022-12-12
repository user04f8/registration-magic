import numpy as np
import queue

from coursedb import CourseDB

class Course:
    def __init__(self, coursedb : CourseDB, college : str, department : str, course_num : int, section : str = None, section_prefs=None):
        """Initializes a Course object storing course information
        
        college: a 3-letter string defining the college, e.g. 'ENG'
        department: a 2-letter string defining the department, e.g. 'EC'
        course_num: an integer defining the course number, e.g. 327, 100 <= course_num <= 999
        section: alphanumeric string defining the section
        """
        
        self.college : str = college
        self.department : str = department
        self.course_num : int = course_num
        if section is None:
            self.section : str
            self.selectit : np.int32
            self.selectit, self.section = coursedb.load_selectit_and_section(college, department, course_num)
        else:
            self.section : str = section
            self.selectit : np.int32 = coursedb.load_selectit(college, department, course_num, section)

        if section_prefs is not None:
            raise NotImplementedError #TODO: selection preferences

    def __str__(self):
        return ' '.join((self.college, self.department, str(self.course_num), (self.section if self.section is not None else '')))

    @staticmethod
    def leftpad(selectit : int) -> str:
        selectit = str(selectit)
        return '0' * (10 - len(selectit)) + selectit

    def getURLparams(self):
        """Return the URL params associated with a course for making a request to the Student Link
        full URL = f'https://www.bu.edu/link/bin/uiscgi_studentlink.pl/{unix_timestamp}' + self.getURLparams(semester) + ...
        e.g.        'https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1668886235?ModuleName=reg%2Fadd%2Fbrowse_schedule.pl&SearchOptionDesc=Class+Number&SearchOptionCd=S&ViewSem=Spring+2023&KeySem=20234&AddPlannerInd=Y&College=CAS&Dept=&Course=000&Section='
        """
        return f'?SelectIt={Course.leftpad(self.selectit)}' # + '&College={self.college}&Dept={self.department}&Course={str(self.course_num)}&Section={self.section}'

class Semester():
    REGISTER_URL_PARAMS = '&ModuleName=reg%2Fadd%2Fconfirm_classes.pl&AddPreregInd=&AddPlannerInd='
    PLAN_URL_PARAMS = REGISTER_URL_PARAMS + '&ModuleName=plan%2Fadd_planner%2Fconfirm_classes.pl&AddPreregInd=&AddPlannerInd=Y'
    BOILERPLATE_URL_PARAMS = '&PreregViewSem=&PreregKeySem=&SearchOptionCd=S&SearchOptionDesc=Class+Number&MainCampusInd=&BrowseContinueInd=&ShoppingCartInd=&ShoppingCartList='
    def __init__(self, semester : str, year : int):
        """Returns a Semester object given a semester and Course objects
        
        semester: a string 'Spring' or 'Fall' (TODO 'Summer')
        int: the year within the semester begins
        """
        #self.semester = semester
        #self.year = year
        self.id : int = Semester.getid(semester, year) # For the User() class to keep a dictionary of semesters
        semester_year = semester + '+' + str(year)
        year_key = str(year) + str(year + 1)[-1]
        # TODO year 2029 problem: I can't test how student link handles the year key 2029-2030, assume it's 20290
        self.semester_url_params : str = f'&ViewSem={semester_year}&KeySem={year_key}'
        self.courses : queue.Queue = queue.Queue()

    @staticmethod
    def getid(semester : str, year : int):
        return (year << 8) + ord(semester[0])

    def add_course(self, course : Course):
        self.courses.put(course)
        return self
    
    def pop_course(self):
        if self.courses.qsize() == 0:
            return None
        else:
            return self.courses.get()
    
    def course_iter(self):
        course = self.pop_course()
        while course is not None:
            yield course
            course = self.pop_course()
        return StopIteration
        
    def getURLparams(self, course : Course, planner=False):
        # TODO write a generator to go through every course in a semseter
        if planner:
            return ''.join((course.getURLparams(), Semester.PLAN_URL_PARAMS, self.semester_url_params, Semester.BOILERPLATE_URL_PARAMS))
            # add 'Y' to AddPlannerInd= to add to planner (not real course registration)
        return ''.join((course.getURLparams(), Semester.REGISTER_URL_PARAMS, self.semester_url_params, Semester.BOILERPLATE_URL_PARAMS))

