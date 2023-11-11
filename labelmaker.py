#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

class Labelmaker:
    def __init__(self, filename: str):
        self._filename = filename
        self.__entries = []
        self.__labels = set()
        self.__make_labels(filename)
        self.__write_to_file()

    def __make_labels(self, filename: str) -> None:
        """
        Opens a .bib file and changes the labels of the entries to
        author year.
        The output file is written to the same location, adding
        "_labelled.bib" to the end of the filename.

        The below pattern captures an entry.
        An entry begins with @. @ is always preceded by a new line except for 
        the first entry.

        Example entries:
        @book{RN123,
        author = {Bresnan, Joan and Asudeh, Ash and Toivonen, Ida and Wechsler, Stephen},
        title = {Lexical-Functional Syntax},
        publisher = {Wiley Blackwell},
        address = {Chichester},
        edition = {2nd},
        year = {2016},
        type = {Book}
        }
        
        @inbook{RN361,
        author = {Rákosi, György},
        title = {Anaphora},
        booktitle = {The Handbook of Lexical Functional Grammar},
        editor = {Dalrymple, Mary},
        series = {Empirically Oriented Theoretical Morphology and Syntax},
        publisher = {Language Science Press},
        address = {Berlin},
        year = {forthcoming},
        type = {Book Section}
    }

        """
        with open(filename) as file:
            entry = ""
            for line in file:
                if line != "}\n": # "}\n" is the final line of an entry
                    # print(line)
                    if line == "\n": # lines between entries are empty
                        continue
                    entry += line
                # elif line == "}": # the final entry might not be followed by a newline
                #     entry += line # adding the final "}\n"
                #     self.__parse_entry(entry)
                else:
                    entry += line # adding the final "}\n"
                    self.__parse_entry(entry)
                    entry = ""
        self.__parse_entry(entry)
        print(self.__labels)

    def __parse_entry(self, entry: str) -> None:
        """
        Takes one entry as an argument.
        Finds author names and year, then changes the label. 
        The updated entry is added to the list self.__entries.
        """
        # print(entry)
        lines = entry.split("\n")
        first_line = lines[0]
        # print("lines[0]", lines[0])
        label_start_index = first_line.find("{") + 1
        # print(first_line[label_start_index:])

        # Authors are always on the second line of an entry, but some works
        # may not have authors. Entries without authors are left as-is.
        if not "author" in lines[1]:
            self.__entries.append(entry)
            return
        
        # This presumes that authors have been added in the way 
        # EndNote specifies, i.e. Firstname Lastname and one author
        # per line. Then we get "and" between authors, e.g.:
        # "Basso, Gaetano and Peri, Giovanni and Rahman, Ahmed S."
        name_start = lines[1].find("{") + 1 # add one since start index is inclusive
        name_end = lines[1].find("}")
        authors = lines[1][name_start:name_end].split(" and ")
        last_names = [author.split(",")[0].lower() for author in authors]

        # finding the year
        date_index = -1
        if "origdate" in entry:
            date_index = entry.find("origdate = {") + 12
        elif "year" in entry:
            date_index = entry.find("year = {") + 8
        elif "date" in entry:
            date_index = entry.find("date = {") + 8
        else:
            year = ""
        # years are lazily assumed to be four digits:
        if date_index != -1:
            year = entry[date_index:date_index+4]
        if year == "fort":
            year = "forthcoming"

        label = self.__create_label(last_names, year)

        # creating an entry with the new label
        first_line = first_line[:label_start_index] + label + ",\n"
        entry = first_line + "\n".join(lines[1:])
        self.__entries.append(first_line.join(lines[1:]))

    
    def __create_label(self, last_names: list[str], year: str) -> str:
        """
        Creates a label.
        If there are three or more authors, the label is the last name of the
        first author + etal + year.
        """        
        if len(last_names) > 2:
            label = last_names[0] + "etal" + year
        else:
            label = "".join(last_names) + year
        
        # checking for duplicates
        if label not in self.__labels:
            self.__labels.add(label)
            return label

        # if there is a duplicate, try adding a letter of the alphabet
        # if there are more duplicates than letters in the alphabet, well...
        duplicate = label
        i = 0
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        while duplicate in self.__labels and i < len(alphabet):
            duplicate = label + alphabet[i]
            i += 1
        
        assert(duplicate not in self.__labels)
        self.__labels.add(duplicate)
        return duplicate
            

    def __write_to_file(self, overwrite=False) -> None:
        ...


    # need to deal with multiple authors somehow. Maybe nice to define a new
    # method for those. Let's say two authors are lastnamelastnameyear, but three or
    # more are lastnameetalyear.
    # this should be doable with a regex that checks how many "and"s are found between
    # the brackets behind author.
    # So the only line I actually need to change is the first line, where I want to
    # enter the new label. The entry type is to be left unchanged.


"""
# I will also have to account for duplicates. A possible way of handling them should
# be to maintain a set of labels that have been used already. If a label is in this
# set, try the label with a added to the end, and so on. I guess having a string
# "abcdefgh..." will suffice, then I can try adding letters to the original label
# suggestion until a label that is not in the set of existing labels is found.
#
# I don't think I'll bother dealing with stuff like "pubstate = forthcoming",
# but since EndNote seems to save forthcoming as year, that should take care of 
# those situations, generally, as "nameforthcoming".
"""
def main(filename):
    Labelmaker(filename)

if __name__ == "__main__": 
    filename = str(sys.argv[1])
    print("Running labelmaker.py with {!r}".format(filename))
    main(filename)