uvic-transcript-parser
======================

Parses plain text UVic transcripts into an SQLite database and allows
exporting data to a CSV file.

This was done as part of CENG 499, capstone project, at UVic
(http://www.ece.uvic.ca/~elec499/2012-summer/Project_Summaries.shtml).
The end goals of the project were to: 

1) identify courses which are key to student success 

2) predict whether a student will successfully graduate based on their 
first year course grades

Data mining and machine learning techniques were used to meet these goals after parsing it into a convenient format.

Usage
-----
To parse transcripts, go to the parser directory and run 'run_cmdln.py'.
It will prompt for inputs as necessary.

To generate a CSV file of first year records, go to the parser directory and 
run 'first_year_csv.py'.  It will also prompt for input files.
