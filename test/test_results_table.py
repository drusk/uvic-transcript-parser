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

import unittest

from parser.results_table import ResultsTable
from parser.csv_util import generate_csv_line

class ResultsTableTest(unittest.TestCase):

    def generate_csv_str(self, table):
        csv_str = ""
        for row in table.rows:
            csv_str += generate_csv_line(row)
        return csv_str

    def testTableContentsOneRow(self):
        expected_csv = ",COL1,COL2,COL3\n1,VAL1,VAL2,VAL3\n"
        column_ids_names = [(1, "COL1"), (2, "COL2"), (3, "COL3")]
        table = ResultsTable(column_ids_names)
        table.add_row(1, {1: "VAL1", 2: "VAL2", 3: "VAL3"})
        self.assertEqual(expected_csv, self.generate_csv_str(table))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'ResultsTableTest.testTableContentsOneRow']
    unittest.main()