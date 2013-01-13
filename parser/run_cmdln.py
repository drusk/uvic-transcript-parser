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

Runs the application with a command line interface.

@author: drusk
'''

import os
import sys

import file_processor

def abort_program(msg):
    '''
    Shuts the program down with an error message.
    '''
    print msg
    print "Aborting program"
    sys.exit(1)

def run():
    '''
    Runs the command line interface.
    '''
    input_path = raw_input("Enter the FULL path to a directory containing " \
                           + "the transcripts, or to a single transcript file: ")

    while not os.path.exists(input_path):    
        input_path = raw_input("Target location does not exist!  " \
                               + "Please enter a valid path: ")
    
    main_database_name = raw_input("Enter the FULL path to the desired " \
                                   + "location of the main database: ")
    
    id_database_name = raw_input("Enter the FULL path to the desired " \
                                 + "location of the database which will " \
                                 + "store student's real-world identifiers: ")
    
    if os.path.isdir(input_path):
        file_processor.process_directory(input_path, main_database_name, id_database_name)
    elif os.path.isfile(input_path):
        file_processor.process_file(input_path, main_database_name, id_database_name)
    else:
        abort_program("Unknown input file or directory")

    print "Finished processing"

if __name__ == "__main__":
    run()
    