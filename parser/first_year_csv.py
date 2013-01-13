# Copyright (C) 2012 David Rusk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.
'''
Created on 2012-06-21

Retrieves first year course grades for students and writes them to a CSV file.

@authors: drusk, Fred Song
'''

import database_interface
from results_table import ResultsTable
from cmd_io_util import get_valid_filename

"""
First year courses
CSC111 / CSC110
CSC115 / CSC160

ELEC199

ENGL135 / ENGL115

MATH100
MATH101
MATH110 / MATH133

MECH141 / ENGR141
PHYS122
PHYS125
CHEM150

ENGR110
ENGR120
"""


# retrieves the course ids for those whose number starts with '1'
GET_FIRST_YEAR_COURSES = "SELECT cid, dept, number FROM Courses WHERE number LIKE '1%'"

# retrieves all the courses each student has taken along with their grades
GET_STUDENT_COURSE_GRADES = "SELECT sid, cid, gradePoint FROM Registration"

# retrieves the sid and label for all students
GET_STUDENT_LABELS = "SELECT sid, classification FROM Students"

# database attribute name for the course id
COURSE_ID = "cid"

# database attribute name for the department offering the course
COURSE_DEPT = "dept"

# database attribute name for the number associated with a course
COURSE_NUM = "number"

# database attribute name for the student id
STUDENT_ID = "sid"

# database attribute name for a student's grade in a course
GRADE = "gradePoint"

def get_first_year_courses(con):
    '''
    Retrieves the ids, department and number for first year courses found in 
    the database whose connection is passed in.
    '''
    cur = con.cursor()
    cur.execute(GET_FIRST_YEAR_COURSES)
    return [(row[COURSE_ID], row[COURSE_DEPT], row[COURSE_NUM]) \
             for row in cur.fetchall()]

def get_student_grades(con, normalizer):
    '''
    Retrieves all grades for all students from the database whose connection 
    is passed in.  A dictionary is returned.  The keys are the student ids.  
    Each value is in turn a dictionary whose keys are the course ids and 
    whose values are the associated grades.
    '''
    all_students_grades = {}
    cur = con.cursor()

    # get student labels
    cur.execute(GET_STUDENT_COURSE_GRADES)
    for row in cur.fetchall():
        sid = row[STUDENT_ID]
        if sid not in all_students_grades:
            all_students_grades[sid] = {}
        student_grades = all_students_grades[sid]
        cid = normalizer.get_norm_cid(row[COURSE_ID])
        if not cid: 
            continue
        grade = row[GRADE]
        # if a student has multiple grades for a course, record the lowest
        if cid not in student_grades or grade < student_grades[cid]:  
            student_grades[cid] = grade
            
    return all_students_grades

class CourseNormalizer(object):
    """ Normalizes and filters a list of courses """
    FIRST_YEAR_COURSES = [
        ("CSC111","CSC110"),
        ("CSC115","CSC160"),
        ("ELEC199",),
        ("ENGL135","ENGL115"),
        ("MATH100",),
        ("MATH101",),
        ("MATH110","MATH133"),
        ("MECH141","ENGR141"),
        ("PHYS122",),
        ("PHYS125",),
        ("CHEM150",),
        ("ENGR110",),
        ("ENGR120",)
    ]
    def __init__(self, course_list):
        """course_list = list of (cid, course_name) tuples"""
        self.name_map = {} # norm_name => norm_cid
        self.cid_map = {}  # cid => (norm_cid, norm_name)

        # make mapping of normalized_coursename => norm_cid
        for r in course_list:
            cid,name = r
            for course in CourseNormalizer.FIRST_YEAR_COURSES:
                if name == course[0]:
                    self.name_map[name] = cid
                    break
        
        def get_normalized_course_name(name):
            for course in CourseNormalizer.FIRST_YEAR_COURSES:
                norm_name = course[0]
                for dup in course:
                    if name == dup:
                        return norm_name
            return None

        for r in course_list:
            cid,name = r
            norm = get_normalized_course_name(name)
            if norm:
                self.cid_map[cid] = (self.name_map[norm], norm)
    
    def get_norm_cid(self, cid):
        if cid not in self.cid_map:
            return None
        return self.cid_map[cid][0]
    
    def get_norm_name(self, cid):
        if cid not in self.cid_map:
            return None
        return self.cid_map[cid][1]

    def get_norm_course_list(self):
        return [(cid,name) for name,cid in self.name_map.iteritems()]
    
def get_student_first_year_course_grades(dbname):
    '''
    Returns a list of lists.  Each sublist represents the grades of one 
    student.  The list has grades for all first year courses.
    '''
    # TODO make None default
    con = database_interface.get_database_connection(dbname, None)
    courses = map(lambda inf: (inf[0], inf[1] + inf[2]), get_first_year_courses(con))
    normalizer = CourseNormalizer(courses)

    columns = normalizer.get_norm_course_list()
    columns.append((-1, "Label"))
    results_table = ResultsTable(columns)
    
    students = get_student_grades(con, normalizer)

    cur = con.cursor()
    cur.execute(GET_STUDENT_LABELS)
    for r in cur:
        sid, label = r
        students[sid][-1] = label

    for sid in students.keys():
        results_table.add_row(sid, students[sid])
    
    con.close()
    return results_table

def generate_csv_file(query_func, dbname, output_filename):
    '''
    Executes a specified function which queries a database and returns a 
    results table.  The results table is then written to the specified output 
    filename.
    '''
    results_table = query_func(dbname)
    results_table.to_csv_file(output_filename)

if __name__ == "__main__":
    dbname = get_valid_filename("Enter the full path to the database", \
                                "File not found.  Try again")
    output_filename = raw_input("Enter the full path to a new desired output file: ")

    generate_csv_file(get_student_first_year_course_grades, \
                      dbname, output_filename)
