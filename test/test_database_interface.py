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

@author: drusk
'''
import unittest

from parser.database_interface import Connection, write_student
from parser.transcript_model import Term, Course, Student

REQ_SATISFIED = "Satisfied"

class DatabaseInterfaceTest(unittest.TestCase):

    def setUp(self):
        self.con = Connection(":memory:", ":memory:")

    def tearDown(self):
        self.con.close()

    def testWriteStudent(self):
        courses = []
        courses.append(Course("CSC", 110, "PROGRAMMING", 1.50, "A+", 9))
        courses.append(Course("MATH", 100, "CALCULUS:I", 1.50, "A+", 9))
        term = Term("WINTER", 2008, 2009, courses)
        terms = [term]
        student = Student("Bob", "V00123456", terms, REQ_SATISFIED, 3.5, "y")
        write_student(student, self.con)
        
        cur = self.con.get_main_con().cursor()
        cur.execute("SELECT COUNT(*) AS count FROM Students")
        studentCount = int(cur.fetchone()["count"])
        self.assertEqual(studentCount, 1)
        
        cur.execute("SELECT sid, currCumulativeGpa, englishReq FROM Students")
        fetch = cur.fetchone()
        currCumulativeGpa = float(fetch["currCumulativeGpa"])
        englishReq = fetch["englishReq"]
        self.assertEqual(currCumulativeGpa, 3.5)
        self.assertEqual(englishReq, REQ_SATISFIED)
        
        cur.execute("SELECT COUNT(*) AS count FROM Terms")
        termCount = int(cur.fetchone()["count"])
        self.assertEqual(termCount, 1)
        
        cur.execute("SELECT COUNT(*) AS count FROM Courses")
        courseCount = int(cur.fetchone()["count"])
        self.assertEqual(courseCount, 2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'ParseRecordTest.testName']
    unittest.main()
    