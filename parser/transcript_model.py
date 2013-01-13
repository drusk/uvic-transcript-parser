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
Created on 2012-05-23

Contains classes for storing extracted transcript data.

@author: drusk
'''
import re

# classification code constants
PROBATION = "p"
SUCCESSFUL = "s"
FAILED = "f"
IN_PROGRESS_OR_INVALID = "i"

# indicator strings from raw text
PROBATION_STANDING = "PROBATION"
FAILED_STANDING = r"(?:REQD|REQUIRED) TO WITHDRAW"

class Course(object):
    '''
    Stores information about a class a student took, as parsed from 
    their transcript.
    '''

    def __init__(self, dept, num, title, credit, grade_point, special_status):
        '''
        Creates a new course record.
        Example input: MATH, 100, CALCULUS:I, 1.50, 9, None
        '''
        self.dept = dept
        self.num = num
        self.title = title
        self.credit = credit
        self.grade_point = grade_point
        self.special_status = special_status
        
    def get_department(self):
        return self.dept
    
    def get_course_number(self):
        return self.num
    
    def get_course_title(self):
        return self.title
    
    def get_credits(self):
        return self.credit
    
    def get_special_status(self):
        return self.special_status
    
    def get_grade_point(self):
        return self.grade_point
    
    def __str__(self):
        return "{" + self.dept + " " + self.num + "}"


class Term(object):
    '''
    Stores information about a term of classes taken by a student, as parsed 
    from their transcript.
    '''

    def __init__(self, season, start_year, end_year, courses):
        '''
        Creates a new term record.
        Example input: WINTER, 2008, 2009, [...]
        '''
        self.season = season
        self.start_year = start_year
        if end_year == None:
            self.end_year = start_year
        else:
            self.end_year = end_year
        self.courses = courses
        self.standing = None
        self.sessional_gpa = None
        self.credits_earned = None
        self.program = None
    
    def apply_session_summary(self, session_summary):
        self.standing = session_summary.get_standing()
        self.sessional_gpa = session_summary.get_sessional_gpa()
        self.credits_earned = session_summary.get_credits_earned()
    
    def set_program(self, program):
        self.program = program
    
    def get_season(self):
        return self.season
    
    def get_start_year(self):
        return self.start_year
    
    def get_end_year(self):
        return self.end_year
    
    def get_courses(self):
        return self.courses
    
    def get_standing(self):
        return self.standing
    
    def get_sessional_gpa(self):
        return self.sessional_gpa
    
    def get_credits_earned(self):
        return self.credits_earned
    
    def get_program(self):
        return self.program
    
    def get_season_year_str(self):
        return self.season + "_" + self.start_year + "-" + self.end_year
    
    def add_course(self, course):
        self.courses.append(course)
        
    def __str__(self):
        return self.get_season_year_str()


class Student(object):
    '''
    Stores all the information for a student that is parsed from their 
    transcript.
    '''
    
    def __init__(self, name, student_number, terms, english_requirement, \
                 cumulative_gpa, credential_granted):
        self.name = name
        self.student_number = student_number
        self.terms = terms
        self.english_requirement = english_requirement
        self.gpa = cumulative_gpa
        self.credential_granted = credential_granted
        
    def get_name(self):
        return self.name
    
    def get_student_number(self): 
        return self.student_number
        
    def get_terms(self):
        return self.terms
    
    def get_english_requirement_status(self):
        return self.english_requirement
    
    def get_current_cumulative_gpa(self):
        return self.gpa
    
    def get_all_courses(self):
        return [course for term in self.terms for course in term.get_courses()]

    def was_on_probation(self):
        '''
        Determines whether the student has ever been on probation.
        '''
        for term in self.terms:
            standing = term.get_standing()
            if standing == None:
                continue
            elif PROBATION_STANDING in standing:
                return True
        return False
    
    def was_required_to_withdraw(self):
        '''
        Determines whether the student was required to withdraw.
        '''
        for term in self.terms:
            standing = term.get_standing()
            if standing == None:
                continue
            elif re.search(FAILED_STANDING, standing) != None:
                return True
        return False

    def get_classification(self):
        '''
        Determines a student's classification code.
        '''
        if self.credential_granted:
            if self.was_on_probation() or self.was_required_to_withdraw():
                return PROBATION
            else:
                return SUCCESSFUL;
        else:
            if self.was_required_to_withdraw():
                return FAILED
            else:
                return IN_PROGRESS_OR_INVALID
    