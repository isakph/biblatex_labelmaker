import re

def make_labels(filename: str) -> None:
    """
    Opens a .bib file and changes the labels of the entries to
    author year, checking for duplicates while doing so.
    The output file is written to the same location, adding
    "labelled" to the end of the filename.
    """
    # The below pattern captures an entry.
    # An entry has a prefix "@entrytype{\n" and a suffix "}\n}\n".
    # The flags m (multiline) and s (match all) ensure that we match line changes.
    entry_pattern = re.compile(r"(?ms)^@\w*\{.*\}\n\}$")
    pattern = re.compile(r"(?ms)@\w+\{\w+,\n(\w+= \{([\w, -]*\},?)\n)+^\}")
    # (\w+= \{([\w, -]*\},?)\n)+ er ment å matche "title = {Lexical-Functional Syntax},\n" osv
    # but pretty sure it doesn't. What characters occur within {}? "," and "-" and
    # what else? "'" can occur, "." can occur (as in O'Connell or l'homme, and Race, William H.)
    # I'll want to split the regexing thing up into at least two things.
    # 1) Find an entry and return it as a match.
    # 2) Rewrite the entry and return it.
    # Then I can write it to a new file.

    """
    Example entry:
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
        for match in re.search(entry_expression, file):


    # need to deal with multiple authors somehow. Maybe nice to define a new
    # method for those. Let's say two authors are lastnamelastnameyear, but three or
    # more are lastnameetalyear.
    # this should be doable with a regex that checks how many "and"s are found between
    # the brackets behind author.
    # So the only line I actually need to change is the first line, where I want to
    # enter the new label. The entrytype can be left unchanged.


"""
# I will also have to account for duplicates. A possible way of handling them should
# be to maintain a set of labels that have been used already. If a label is in this
# set, try the label with a added to the end, and so on. I guess having a string
# "abcdefgh..." will suffice, then I can try adding letters to the original label
# suggestion until a label that is not in the set of existing labels is found.
#
# I don't think I'll bother dealing with stuff like "pubstate = forthcoming",
# but since EndNote seems to save forthcoming as year, then
"""
