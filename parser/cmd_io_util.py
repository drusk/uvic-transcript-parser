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
Created on 2012-06-19

Provides utility methods for working with command line specified input 
and output.

@author: drusk
'''

import os

def get_valid_input(initial_msg, condition_func, fail_msg):
    '''
    Prompts the user for input by displaying initial_msg.  The input is 
    validated using condition_func, which should take the input and return a 
    boolean value.  While the input is not valid, the user will be prompted 
    to try again with the fail_msg.
    '''
    user_in = raw_input(initial_msg + ": ")
    while not condition_func(user_in):
        user_in = raw_input(fail_msg + ": ")
    return user_in

def get_valid_filename(initial_msg, fail_msg):
    '''
    Prompts the user for a file name by displaying initial_msg.  If the input 
    is an existing file, it is returned.  As long as the input is not an 
    existing file, the user will be prompted to try again with the fail_msg.
    '''
    return get_valid_input(initial_msg, os.path.exists, fail_msg)
