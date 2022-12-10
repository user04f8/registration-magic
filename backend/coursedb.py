import numpy as np
import pandas as pd

class CourseNotFoundException(Exception):
    """Exception for CourseDB not finding a given course"""
    pass

class CourseDB:
    SELECTIT = 'SelectIt'
    COLLEGE = 'College'
    DEPARTMENT = 'Department'
    COURSE_NUM = 'CourseNum'
    SECTION = 'Section'
    COLUMN_ITER = ((SELECTIT, np.int32), (COLLEGE, str), (DEPARTMENT, str), (COURSE_NUM, int), (SECTION, str))

    def __init__(self, filename : str, sheetname : str = 'Sheet1'):
        self.course_df = pd.read_excel(io=filename, sheet_name=sheetname)
        for column, t in CourseDB.COLUMN_ITER:
            self.course_df[column] = self.course_df[column].astype(t)

    def load_selectit(self, college : str, department: str, course_num : int, section : str) -> int:
        df = self.course_df
        df = df[(df[CourseDB.COLLEGE]==college) & (df[CourseDB.DEPARTMENT]==department) & (df[CourseDB.COURSE_NUM]==course_num) & (df[CourseDB.SECTION]==section)]
        if __debug__:
            if len(df) > 1:
                print(f'Warning: duplicate course {college} {department}{course_num} {section} exists {len(df)} times')
        if len(df) == 0:
            raise CourseNotFoundException(f'Course {college} {department}{course_num} {(section if section else "")} not found.')

        selectit = df[CourseDB.SELECTIT].iloc[0]
        # unwrap the (hopefully) single row dataframe into a row and get the SELECTIT value 
        # int() is necessary to bring the numpy.int32 down to a python int

        return selectit

    def load_selectit_and_section(self, college : str, department: str, course_num : int) -> int:
        df = self.course_df
        df = df[(df[CourseDB.COLLEGE]==college) & (df[CourseDB.DEPARTMENT]==department) & (df[CourseDB.COURSE_NUM]==course_num)]
        idx = 0 # TODO : intelligently find the best section (replace idx with the value with the most open seats)
        section = df[CourseDB.SECTION].iloc[idx]
        if len(df) == 0:
            raise CourseNotFoundException(f'Course {college} {department}{course_num} {(section if section else "")} not found.')

        selectit = df[CourseDB.SELECTIT].iloc[idx]
        # unwrap the (hopefully) single row dataframe into a row and get the SELECTIT value 
        # int() is necessary to bring the numpy.int32 down to a python int

        return selectit, section