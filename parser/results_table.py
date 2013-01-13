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
Created on 2012-06-26

@author: drusk
'''

from csv_util import write_csv_file

class ResultsTable(object):
    '''
    Models results found as rows and columns which can be written to a CSV 
    file.
    '''
    
    def __init__(self, column_ids_names):
        '''
        Initializes the table with the specified columns.  Column display 
        names may be different than the column ids.  The ids and names should 
        be passed in as a list of tuples in the form (id, name).
        '''
        self.column_ids = [item[0] for item in column_ids_names]
        title_row = [""]
        title_row.extend([item[1] for item in column_ids_names])
        self.rows = []
        self.rows.append(title_row)
        
    def add_row(self, row_id, vals_by_column_id):
        '''
        Adds a row of data to the table.  The values are passed as a map from 
        the column ids to the specific values found in this row.  A row 
        identifier is also passed in.
        '''
        row_vals = [row_id]
        for column_id in self.column_ids:
            if column_id in vals_by_column_id:
                value = vals_by_column_id[column_id]
                if value == None:
                    row_vals.append("")
                else:
                    row_vals.append(value)
            else:
                row_vals.append("")
        self.rows.append(row_vals)
    
    def to_csv_file(self, filename):
        '''
        Writes the table to a CSV file with the specified name.
        '''
        write_csv_file(self.rows, filename)
