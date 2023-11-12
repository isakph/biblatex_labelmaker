#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
from unidecode import unidecode

class Labelmaker:
    def __init__(self, filename: str):
        self.__filename = filename
        self.__entries = []
        self.__labels = set()
        self.__make_labels(filename)
        self.__write_to_file()

    def __make_labels(self, filename: str) -> None:
        """
        Opens a .bib file and changes the labels of the entries to
        authoryear.
        The output file is written to the same location, adding
        "_labelled.bib" to the end of the filename.

        The below pattern captures an entry.
        An entry begins with @. @ is always preceded by a new line except for 
        the first entry. For further details about entries, see test.txt which 
        contains a few variations.

        EndNote automatically adds two newlines to the end of the document.
        """
        with open(filename) as file:
            entry = ""
            for line in file:
                if line != "}\n": # "}\n" is the final line of an entry
                    if line == "\n": # lines between entries are empty
                        continue
                    entry += line
                else:
                    entry += line # adding the final "}\n"
                    self.__parse_entry(entry)
                    entry = ""

    def __parse_entry(self, entry: str) -> None:
        """
        Takes one entry as an argument.
        Finds author names and year, then changes the label. 
        The updated entry is added to the list self.__entries.
        """
        lines = entry.split("\n")
        first_line = lines[0]
        label_start_index = first_line.find("{") + 1

        # Authors are always on the second line of an entry, but some works
        # may not have authors. Entries without authors are left as-is.
        if not "author" in lines[1]:
            self.__entries.append(entry)
            return
        
        # This presumes that authors have been added in the way 
        # EndNote specifies, i.e. Firstname Lastname and one author
        # per line. Then EndNote produces an "and" between authors, e.g.:
        # "Basso, Gaetano and Peri, Giovanni and Rahman, Ahmed S."
        name_start = lines[1].find("{") + 1 # add one since start index is inclusive
        name_end = lines[1].find("}")
        authors = lines[1][name_start:name_end].split(" and ")
        
        # This list comprehension normalizes the author names.
        # After splitting on comma, the first element is the last name.
        # unidecode() replaces non-ASCII characters.
        # Labels are lowercase. If an author's last name has a space, 
        # it is replaced with an empty string.
        last_names = [unidecode(author.split(",")[0].lower().replace(" ", "")) for author in authors]
        # we also need to remove any punctuation from the last names:
        last_names = [name.translate(str.maketrans('', '', string.punctuation)) for name in last_names]

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
        # Years are lazily assumed to be four digits, so if the year is "forthcoming",
        # then that has to be fixed.
        if date_index != -1:
            year = entry[date_index:date_index+4]
        if year == "fort":
            year = "forthcoming"

        label = self.__create_label(last_names, year)

        # creating an entry with the new label
        first_line = first_line[:label_start_index] + label + ",\n"
        entry = first_line + "\n".join(lines[1:])
        self.__entries.append(entry)

    
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

        # if there is a duplicate, try adding a letter of the alphabet.
        # If there are more duplicates than letters in the alphabet,
        # the below assertion raises an error.
        duplicate = label
        i = 0
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        while duplicate in self.__labels and i < len(alphabet):
            duplicate = label + alphabet[i]
            i += 1
        
        assert(duplicate not in self.__labels) # too many duplicates?
        self.__labels.add(duplicate)
        return duplicate
            

    def __write_to_file(self, overwrite=False) -> None:
        with open(self.__filename.split(".")[0] + "_labelled.bib", "w") as file:
            file.write("\n".join(self.__entries))


def main(filename):
    Labelmaker(filename)

if __name__ == "__main__": 
    filename = str(sys.argv[1])
    print("Running labelmaker.py with {!r}".format(filename))
    main(filename)
