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
Created on 2012-06-20

Methods for working with CSV files.

@author: drusk
'''

def generate_csv_line(list_values):
    '''
    Turns a list of values into a string formatted as a line ready to be 
    written to a CSV file.  Has a newline at the end.
    '''
    csv_line = ""
    for i, val in enumerate(list_values):
        csv_line += str(val)
        if i < len(list_values) - 1:
            csv_line += ","
    csv_line += "\n"
    return csv_line

def write_csv_file(list_of_lists, filename):
    '''
    Takes a list of lists.  The sublists should each correspond to a line 
    in the CSV file.  Writes to a file with the specified filename.
    '''
    file_obj = open(filename, "wb")
    for list_vals in list_of_lists:
        file_obj.write(generate_csv_line(list_vals))
    file_obj.close()
