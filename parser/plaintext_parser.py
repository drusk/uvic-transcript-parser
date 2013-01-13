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

Parses student records from the plain text version of their transcript.

@author: drusk
'''

import re

from transcript_model import Course, Term, Student

# retrieves student identification groups:
# 1. student number (ex: V00123456)
# 2. name (ex: John A. Smith)
STUDENT_INFO_REG = r"(V00\d+) ([\w \.]+)"
student_p = re.compile(STUDENT_INFO_REG)

# retrieves whether the English requirement has been satisfied
# 1. requirement satisfied or not (ex: Satisfied)
ENG_REQ_REG = r"(?:ENGLISH|ACADEMIC WRITING) REQUIREMENT\s+Requirement: ([\w ]+)"
engreq_p = re.compile(ENG_REQ_REG)

# retrieves a the student's cumulative gpa
# 1. cumulative GPA (ex: 3.69)
CUMULATIVE_GPA_REG = r"CUMULATIVE GPA : (\d\.\d{2})"
cumulativegpa_p = re.compile(CUMULATIVE_GPA_REG)

# extracts a chunk of text related to a term, into the following groups:
# 1. season (ex: WINTER)
# 2. start year (ex: 2011)
# 3. end year (ex: 2012)
# 4. the rest of the term text (including courses, program, sessional credits and gpa, standing, etc)
TERM_EXTRACT_REG = r"(SUMMER|WINTER) (\d{4})(?:-(\d{4}))?((?:\n[ \t]+[\w \.()\-\t\+\-\:\=,\/]+)+)"
term_extract_p = re.compile(TERM_EXTRACT_REG)

# retrieves course data groups:
#  1. department (ex: CSC)
#  2. number (ex: 370)
#  3. title (ex: DATABASE SYSTEMS)
#  4. unit value (ex: 1.50)
#  5. letter grade (ex: A+)
#  6. grade point (ex: 9)
#  7. awarded units (ex: 1.50)
COURSE_REG = r"(\w{3,4})\s+(\d{3}[a-zA-Z]?)\s+([\w\+\-: ]+)\s+(\d\.\d{2})\s+([\w\+\-]+)\s*(\d)?\s*(\d\.\d{2})?"
course_p = re.compile(COURSE_REG)

# retrieves sessional summary information
# 1. number of credits (ex: 15.00)
# 2. sessional GPA (ex: 4.00)
# 3. standing (ex: "IN GOOD ACADEMIC STANDING", "PLACED ON FACULTY PROBATION")
SESSIONSUMMARY_REG = r"Credit in (\d{1,2}\.\d{2}) Units\s+Sessional GPA = (\d\.\d{2})\s+([\w :\-]+)"
sessionsummary_p = re.compile(SESSIONSUMMARY_REG)

# retrieves the program the student is enrolled in
# 1. program title, beginning with \n and possibly spanning several lines
#PROGRAM_REG = r"(?:SUMMER|WINTER) \d{4}(?:-\d{4})?((?:\n  [\w \.\-()]+)+)"
PROGRAM_REG = r"((?:\n  [\w \.\-()]+)+)"
program_p = re.compile(PROGRAM_REG)

PROGRAM_DELIMITER = " Cooperative Education Work Term Details"

CRED_GRANTED = r"Credential Granted:\s+\d{2} \w{3} \d{4}\s+BACHELOR OF ENGINEERING"
cred_granted_p = re.compile(CRED_GRANTED)

class TermExtract(object):
    '''
    Stores partial results of parsing a term.
    '''
    
    def __init__(self, season, start_year, end_year, term_text):
        '''
        Creates a new term extract.  term_text is the remaining 
        text to be parsed, which contains courses, etc.
        '''
        self.season = season
        self.start_year = start_year
        self.end_year = end_year
        self.term_text = term_text
    
    def get_season(self):
        return self.season
    
    def get_start_year(self):
        return self.start_year
    
    def get_end_year(self):
        return self.end_year
    
    def get_term_text(self):
        return self.term_text

class SessionSummary(object):
    '''
    Stores results of parsing a session for its summary information.
    '''
    
    def __init__(self):
        self.credits_earned = None
        self.sessional_gpa = None
        self.standing = None
        
    def set_credits_earned(self, credits_earned):
        self.credits_earned = credits_earned
    
    def set_sessional_gpa(self, sessional_gpa):
        self.sessional_gpa = sessional_gpa
        
    def set_standing(self, standing):
        self.standing = standing
        
    def get_credits_earned(self):
        return self.credits_earned
    
    def get_sessional_gpa(self):
        return self.sessional_gpa
    
    def get_standing(self):
        return self.standing

def parse_student_id(transcript_string):
    '''
    Extracts a student's name and student identification number from their 
    full transcript in string format.
    Student number is returned first, name second.
    '''
    student_num = None
    name = None
    match = student_p.search(transcript_string)
    if match != None:
        student_num = match.group(1)
        name = match.group(2)
    return student_num, name

def parse_credential_granted(transcript_string):
    '''
    Checks if the student has had an Engineering degree granted to them.
    '''
    return cred_granted_p.search(transcript_string) != None

def parse_english_requirement(transcript_string):
    '''
    Extracts whether the student has met the university's English requirement
    from their full transcript_string in string format.
    '''
    match = engreq_p.search(transcript_string)
    if match != None:
        return match.group(1)

def parse_cumulative_gpa(transcript_string):
    '''
    Extracts the student's cumulative gpa from their full transcript 
    in string format.
    '''
    cumulative_gpa = None
    match = cumulativegpa_p.search(transcript_string)
    if match != None:
        cumulative_gpa = match.group(1)
    return cumulative_gpa

def parse_session_summary(term_text):
    '''
    Takes as input the text associated with a term, and looks for session
    summary information, ie. credits earned that session, sessional GPA and 
    academic standing after that session.
    '''
    session_summary = SessionSummary()
    match = sessionsummary_p.search(term_text)
    if match != None:
        session_summary.set_credits_earned(match.group(1))
        session_summary.set_sessional_gpa(match.group(2))
        session_summary.set_standing(match.group(3))
    return session_summary

def parse_program(term_text):
    '''
    Attempts to parse the program the student is enrolled in for the text
    associated with that term.
    '''
    program = None
    match = program_p.search(term_text)
    if match != None:
        program = match.group(1).strip()
        program = re.sub(r"\s+", " ", program)
        program = program.split(PROGRAM_DELIMITER)[0]
    return program

def parse_courses(term_text):
    '''
    Finds courses and their associated grades from within the text found to 
    be part of a term.
    '''
    courses = []
    for match in re.finditer(course_p, term_text):
        dept = match.group(1)
        num = match.group(2)
        title = match.group(3)
        credit = match.group(4)
        status = match.group(5)
        grade_point = match.group(6)

        # if it is just a regular letter grade it is not a special status
        # if it is something like "COM" or "CONTINUING" it is a special status
        special_status = None if len(status) < 3 else status
        if special_status != None:
            # grade point is not meaningful
            grade_point = None
            
        courses.append(Course(dept, num, title, credit, grade_point, special_status))
    
    return courses

def get_term_extracts(file_string):
    '''
    Finds terms within the transcript and parses their basic structure
    to be stored in a TermExtract object.  Further parsing will be done 
    on the term_text.
    '''
    term_extracts = []
    for match in re.finditer(term_extract_p, file_string):
        term_extracts.append(TermExtract(match.group(1), match.group(2), \
                                         match.group(3), match.group(4)))
    return term_extracts

def process_term_extract(term_extract):
    '''
    Coordinates further parsing of a TermExtract object's term_text.
    Returns a Term object.
    '''
    term_text = term_extract.get_term_text()
    courses = parse_courses(term_text)
    session_summary = parse_session_summary(term_text)
    program = parse_program(term_text)
    term = Term(term_extract.get_season(), term_extract.get_start_year(), \
                term_extract.get_end_year(), courses)
    term.apply_session_summary(session_summary)
    term.set_program(program)
    return term

def read_file_to_string(file_obj):
    '''
    Takes a file object and reads it into a string
    '''
    file_obj.seek(0)
    return file_obj.read()

def convert_to_unix_newlines(string):
    '''
    Converts occurrences of \r\n to \n in a given string.  If the string 
    already has the right formatting, nothing happens.
    ''' 
    return string.replace("\r\n", "\n")

def parse_records(transcript_file):
    '''
    Reads a file containing a student's transcripts and returns the parsed 
    data.
    '''
    transcript_string = convert_to_unix_newlines(read_file_to_string(transcript_file))

    student_number, name = parse_student_id(transcript_string)
    eng_req = parse_english_requirement(transcript_string)
    cumulative_gpa = parse_cumulative_gpa(transcript_string)
    credential_granted = parse_credential_granted(transcript_string)

    terms = []
    for term_extract in get_term_extracts(transcript_string):
        terms.append(process_term_extract(term_extract))
        
    return Student(name, student_number, terms, eng_req, cumulative_gpa, credential_granted)
