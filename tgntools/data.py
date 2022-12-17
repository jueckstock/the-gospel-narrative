'''Tools for parsing/expanding machine-readable Bible databases.
'''
from __future__ import annotations
import os
import re
from collections import defaultdict, namedtuple
from typing import TextIO

# Calculate the path to our default Bible
# (unless overridden by ENVIRONMENT)
_tgntools_dir = os.path.dirname(__file__)
_main_project_dir = os.path.join(_tgntools_dir, "..")
_default_file = os.path.join(_main_project_dir, "data", "kjvdat.txt")
BIBLE_FILE = os.environ.get("BIBLE_FILE", _default_file)


# Simple types and compiled regexen
###################################

VerseRef = namedtuple("VerseRef", ("book", "chapter", "verse"))
Verse = namedtuple("Verse", ("book", "chapter", "verse", "text"))

RX_VLINE = re.compile(r"^([^|]+)\|([^|]+)\|([^|]+)\|\s+([^~]+)~\s*$")


def parse_verse_line(line: str) -> Verse:
    '''Parse a verse-database line of text into a Verse.

    Raises a SyntaxError if the required pattern doesn't match.
    '''
    m = RX_VLINE.match(line)
    if not m:
        raise SyntaxError(f"invalid verse line '{line}'")
    return Verse(m.group(1), int(m.group(2)), int(m.group(3)), m.group(4))


class BibleBooks:
    '''Load/access book spans from a Bible verse database.
    
    Uses the `kjvdat.txt` file format described in `README.md`.
    '''
    def __init__(self, stream: TextIO):
        self._verses = {}
        self._books = {}

        cur_book = None
        max_verses = {}
        cur_chapter = None
        last_verse = None
        for line in stream:
            book, chapter, verse, text = parse_verse_line(line)
            self._verses[VerseRef(book, chapter, verse)] = text
            
            if chapter != cur_chapter:
                if cur_chapter:
                    max_verses[cur_chapter] = last_verse
                cur_chapter = chapter
           
            if book != cur_book:
                if cur_book:
                    self._books[cur_book] = max_verses 
                    max_verses = {}
                cur_book = book
            last_verse = verse

    @staticmethod
    def fromfile(filename: str = BIBLE_FILE) -> BibleBooks:
        with open(filename, "rt", encoding="utf8") as fd:
            return BibleBooks(fd)
    
    def last_chapter(self, book: str) -> int:
        return max(self._books[book])

    def last_verse(self, book: str, chapter: int) -> int:
        return self._books[book][chapter]

    def __getitem__(self, ref: VerseRef) -> str:
        return self._verses[ref]

