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
Created on 2012-06-10

Processes files or directories of files to be parsed and stored in the 
database.

@author: drusk
'''

import os

import plaintext_parser
import database_interface
from database_interface import Connection

def parse_file_to_DB(filename, con):
    '''
    Takes in a the name of a file and a special database Connection which 
    actually has connections to both the main database and id database.  
    Reads the file and parses it, then writes the parsed data to the database.
    '''
    transcript_file = open(filename, 'rb')
    studentRecords = plaintext_parser.parse_records(transcript_file)
    transcript_file.close()
    database_interface.write_student(studentRecords, con)
    con.commit()
    
def process_file(filename, main_database_name, id_database_name):
    '''
    Processes a single file for transcript information.
    '''
    con = Connection(main_database_name, id_database_name)
    parse_file_to_DB(filename, con)
    con.close()

def process_directory(dirname, main_database_name, id_database_name):
    '''
    Processes all the files in a specified directory for transcript 
    information.
    '''
    con = Connection(main_database_name, id_database_name)
    for entry in os.listdir(dirname):
        full_entry = dirname + os.sep + entry
        if os.path.isfile(full_entry):
            print "Processing %s" %entry
            parse_file_to_DB(full_entry, con)
    con.close()
    