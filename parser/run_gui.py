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
Created on 2012-06-07

Used to run the application.  Provides a simple interface for selecting the 
transcripts to parse and the database to put them in.

@author: drusk
'''
import os
import sys

from Tkinter import Tk
from tkFileDialog import askopenfilename, asksaveasfilename, askdirectory
from tkMessageBox import askyesno

import file_processor

def get_input_filename(prompt_message):
    '''
    Prompts the user for a filename.
    '''
    return askopenfilename(title=prompt_message)

def get_input_directory(prompt_message):
    '''
    Prompts the user for a directory.
    '''
    return askdirectory(title=prompt_message)
    
def get_save_filename(prompt_message):
    '''
    Prompts user for save location and file name.
    '''
    return asksaveasfilename(title=prompt_message)

def get_main_database_name():
    '''
    Prompts the user for the name and location of the database to use.
    '''
    return get_save_filename("Choose database name and location.\n" \
                             + "Select an existing database to add to it.")

def get_id_database_name():
    '''
    Prompts the user for the name of a second database in which the real-world 
    identifiers of students will be separately stored.
    '''
    return get_save_filename("Choose a second database name and location for real-world ids")

def abort_program(msg):
    '''
    Shuts the program down with an error message.
    '''
    print msg
    print "Aborting program"
    sys.exit(1)

if __name__ == "__main__": 
    # don't want a full GUI
    Tk().withdraw()
    
    input_is_dir = askyesno(message="Do you want to parse multiple transcripts?")
    
    if input_is_dir:
        dirname = get_input_directory("Select directory containing transcripts")
        if os.path.isdir(dirname):
            main_database_name = get_main_database_name()
            id_database_name = get_id_database_name()
            file_processor.process_directory(dirname, main_database_name, \
                                             id_database_name)
        else:
            abort_program("Not a directory")
            
    else:    
        filename = get_input_filename("Select transcript")
        if os.path.isfile(filename):
            main_database_name = get_main_database_name()
            id_database_name = get_id_database_name()
            file_processor.process_file(filename, main_database_name, \
                                        id_database_name)
        else:
            abort_program("Not a file")
