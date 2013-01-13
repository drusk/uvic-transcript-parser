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

Provides methods for working with the database which extracted records will 
be written to.

@author: drusk
'''

import os.path
import sqlite3 as dblib

CREATE_MAIN_DB = ".." + os.sep + "sql" + os.sep + "create_transcript_tables.sql"
CREATE_ID_DB = ".." + os.sep + "sql" + os.sep + "create_id_table.sql"

class Connection(object):
    '''
    Manages both a connection to the main database as well as to the secondary 
    id database.
    '''
    
    def __init__(self, main_database_name, id_database_name):
        self.main_con = get_database_connection(main_database_name, CREATE_MAIN_DB)
        self.id_con = get_database_connection(id_database_name, CREATE_ID_DB)
        
    def get_main_con(self):
        return self.main_con
    
    def get_id_con(self):
        return self.id_con
    
    def commit(self):
        self.main_con.commit()
        self.id_con.commit()
        
    def close(self):
        self.main_con.close()
        self.id_con.close()

def create_database(con, sqlfile):
    '''
    Creates the tables for the database using the specified sql file.
    '''
    main_sqlfile = open(os.path.dirname(__file__) + os.sep + \
                   sqlfile, "rb")
    sql = main_sqlfile.read()
    main_sqlfile.close()
    con.cursor().executescript(sql)

def get_database_connection(database_name, sqlfile):
    '''
    Establishes a connection to the database with the specified name if it 
    already exists, or creates it if it does not.  The sqlfile is the name 
    of the sql script to be run if the database needs to be created.
    '''
    db_exists = os.path.exists(database_name)
    con = dblib.connect(database_name)
    if not db_exists:
        create_database(con, sqlfile)
        
    # configure for easy row access in result sets
    con.row_factory = dblib.Row
    return con

def get_tid(term, con):
    '''
    Finds out with the term id used in the database for a specified Term object.
    '''
    cur = con.cursor()
    cur.execute("SELECT tid FROM Terms WHERE season=? AND startYear=?" + \
                " AND endYear=?", (term.get_season(), term.get_start_year(), \
                                   term.get_end_year()))
    fetch = cur.fetchone()
    return None if fetch == None else fetch["tid"]

def get_cid(course, con):
    '''
    Finds out with the course id used in the database for a specified Course object.
    '''
    cur = con.cursor()
    cur.execute("SELECT cid FROM Courses WHERE dept=? AND number=?", \
                (course.get_department(), course.get_course_number()))
    fetch = cur.fetchone()
    return None if fetch == None else fetch["cid"]

def get_max_sid(con):
    '''
    Looks up the largest value for sid (student id) in the Students table of 
    the database
    '''
    cur = con.cursor()
    cur.execute("SELECT MAX(sid) AS sid FROM Students")
    return cur.fetchone()["sid"]

def add_term(term, con):
    '''
    Adds the relevant data from a Term object to the Terms table in the 
    database.  This does not include student-specific information.
    '''
    cur = con.cursor()
    cur.execute("INSERT INTO Terms(tid, season, startYear, endYear) VALUES(NULL, ?, ?, ?)", \
                (term.get_season(), term.get_start_year(), term.get_end_year()))

def add_course(course, con):
    '''
    Adds the relevant data from a Course object to the Courses table in the 
    database.  This does not include student-specific information.
    '''
    cur = con.cursor()
    cur.execute("INSERT INTO Courses(cid, dept, number, credits) VALUES(NULL, ?, ?, ?)", \
                (course.get_department(), course.get_course_number(), course.get_credits()))

def add_student(student, con):
    '''
    Adds student-specific data to the relevant tables in the database.
    '''
    main_con = con.get_main_con()
    cur = main_con.cursor()
    cur.execute("INSERT INTO Students(sid, currCumulativeGpa, englishReq, classification) VALUES(NULL, ?, ?, ?)", \
                [student.get_current_cumulative_gpa(), student.get_english_requirement_status(), \
                 student.get_classification()])
    
    # XXX better way to figure out the sid that was just generated?
    sid = get_max_sid(main_con)
    for term in student.get_terms():
        tid = get_tid(term, main_con)
        for course in term.get_courses():
            cid = get_cid(course, main_con)
            cur.execute("INSERT INTO Registration(sid, cid, tid, gradePoint, specialStatus) " \
                        + "VALUES(?, ?, ?, ?, ?)", (sid, cid, tid, course.get_grade_point(), \
                                                    course.get_special_status()))
            
    for term in student.get_terms():
        tid = get_tid(term, main_con)
        cur.execute("INSERT INTO TermStatus(sid, tid, standing, sessionalGpa, creditsEarned, program) " \
                    + "VALUES(?, ?, ?, ?, ?, ?)", (sid, tid, term.get_standing(), term.get_sessional_gpa(), \
                                                   term.get_credits_earned(), term.get_program()))

    # write the student's real world info into the separate id database
    con.get_id_con().cursor().execute("INSERT INTO StudentIds(sid, studentNumber, studentName) " \
                                      + "VALUES(?, ?, ?)", (sid, student.get_student_number(), \
                                                         student.get_name()))

def write_student(student, con):
    '''
    Writes a Student object to the database.  Any information about Terms or 
    Courses they have completed which is not already in the database is added.
    '''
    main_con = con.get_main_con()
    for term in student.get_terms():
        if get_tid(term, main_con) == None:
            add_term(term, main_con)
        
        for course in term.get_courses():
            if get_cid(course, main_con) == None:
                add_course(course, main_con)
                
    add_student(student, con)
