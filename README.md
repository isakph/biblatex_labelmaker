# Biblatex labelmaker
Takes a .bib-file and replaces labels with nameyear (lowercase). When there are two authors, then the label is the two lastnames + year. When there are three or more authors, the label is the last name of the first author + etal + year.
The idea is that this is easier to use than something like EndNote's default, which is to use the EndNote ID as the label.

Run the program from the command line with the filename as an argument, e.g.
`$ python3 labelmaker.py test.txt`
