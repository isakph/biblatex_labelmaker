import regex as re

@staticmethod
def make_labels(filename: str) -> None:
    """
    Opens a .bib file and changes the labels of the entries to
    author year, checking for duplicates while doing so.
    The output file is written to the same location, adding
    "labeled" to the end of the filename.
    """
    # the below pattern captures an entry
    pattern = r"" #TODO: the whole thing
