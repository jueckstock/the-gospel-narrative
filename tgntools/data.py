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

# TODO: move out to JSON formatted file that can be user-specified
BOOK_NAMES = {
    "Gen": "Genesis",
    "Exo": "Exodus",
    "Lev": "Leviticus",
    "Num": "Numbers",
    "Deu": "Deuteronomy",
    "Jos": "Joshua",
    "Jdg": "Judges",
    "Rut": "Ruth",
    "Sa1": "I Samuel",
    "Sa2": "II Samuel",
    "Kg1": "I Kings",
    "Kg2": "II Kings",
    "Ch1": "I Chronicles",
    "Ch2": "II Chronicles",
    "Ezr": "Ezra",
    "Neh": "Nehemiah",
    "Est": "Esther",
    "Job": "Job",
    "Psa": "Psalm", # not Psalms: for references, we mean a _single_ Psalm, not all of them
    "Pro": "Proverbs",
    "Ecc": "Ecclesiastes",
    "Sol": "Song of Solomon",
    "Isa": "Isaiah",
    "Jer": "Jeremiah",
    "Lam": "Lamentations",
    "Eze": "Ezekiel",
    "Dan": "Daniel",
    "Hos": "Hosea",
    "Joe": "Joel",
    "Amo": "Amos",
    "Oba": "Obadiah",
    "Jon": "Jonah",
    "Mic": "Micah",
    "Nah": "Nahum",
    "Hab": "Habbakkuk",
    "Zep": "Zephaniah",
    "Hag": "Haggai",
    "Zac": "Zachariah",
    "Mal": "Malachi",
    "Mat": "Matthew",
    "Mar": "Mark",
    "Luk": "Luke",
    "Joh": "John",
    "Act": "Acts",
    "Rom": "Romans",
    "Co1": "I Corinthians",
    "Co2": "II Corinthians",
    "Gal": "Galatians",
    "Eph": "Ephesians",
    "Phi": "Phillippians",
    "Col": "Colossians",
    "Th1": "I Thessalonians",
    "Th2": "II Thessalonians",
    "Ti1": "I Timothy",
    "Ti2": "II Timothy",
    "Tit": "Titus",
    "Plm": "Philemon",
    "Heb": "Hebrews",
    "Jam": "James",
    "Pe1": "I Peter",
    "Pe2": "II Peter",
    "Jo1": "I John",
    "Jo2": "II John",
    "Jo3": "III John",
    "Jde": "Jude",
    "Rev": "Revelation",
}


def parse_verse_line(line: str) -> Verse:
    '''Parse a verse-database line of text into a Verse.

    Raises a SyntaxError if the required pattern doesn't match.
    '''
    m = RX_VLINE.match(line)
    if not m:
        raise SyntaxError(f"invalid verse line '{line}'")
    return Verse(m.group(1), int(m.group(2)), int(m.group(3)), m.group(4))


# TODO: replace "BibleBooks" class with two classes: BibleMap and BibleText
# BibleText will just load up a kjvdat.txt-format file for verse lookup by VerseRef
# BibleMap will load from JSON (or other supported formats) a database of books
# and chapter/verse limits allowing us to do things like:
#   - tell if a reference is legal
#   - tell if two references are contiguous
#   - generate the sequence of all references between two valid, non-contiguous references
#   - translate a book abbreviation into its "pretty name" (for references)

# also TODO, modify __main__.py to become a git-like multi-tool:
#   - "typeset" (the current functionality of taking an edit list, Bible data, and typesetter config and producing typeset output)
#   - "map": new tool parsing a kjvdat.txt file and producing a "biblemap.json" file, containing a JSON object of book-abbrev -> { pretty_name: "", chapter_limits: [verses-in-chap1, ..]}, for use with the BibleMap class; the "pretty_name" will, of course, be left empty for human to fill in



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
        max_verses[chapter] = last_verse
        self._books[book] = max_verses

    @staticmethod
    def fromfile(filename: str = BIBLE_FILE) -> BibleBooks:
        with open(filename, "rt", encoding="utf8") as fd:
            return BibleBooks(fd)
    
    def last_chapter(self, book: str) -> int:
        return max(self._books[book])

    def last_verse(self, book: str, chapter: int) -> int:
        return self._books[book][chapter]

    def is_valid_ref(self, v: VerseRef) -> bool:
        if v.book not in self._books:
            return False
        if v.chapter not in self._books[v.book]:
            return False
        if v.verse < 1 or v.verse > self._books[v.book][v.chapter]:
            return False
        return True

    def get_next_ref(self, v: VerseRef) -> VerseRef:
        inc_verse = VerseRef(v.book, v.chapter, v.verse + 1)
        if self.is_valid_ref(inc_verse):
            return inc_verse
        inc_chapter = VerseRef(v.book, v.chapter + 1, 1)
        if self.is_valid_ref(inc_chapter):
            return inc_chapter
        book_seq = list(self._books)
        book_i = book_seq.index(v.book)
        inc_book = VerseRef(book_seq[book_i + 1], 1, 1)
        if self.is_valid_ref(inc_book):
            return inc_book
        raise StopIteration()

    def refs_are_congituous(self, v1: VerseRef, v2: VerseRef) -> bool:
        return self.get_next_ref(v1) == v2 

    def pretty_name(self, abbrev: str) -> str:
        return BOOK_NAMES[abbrev]

    def __getitem__(self, ref: VerseRef) -> str:
        return self._verses[ref]

