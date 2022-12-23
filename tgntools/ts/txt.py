"""Plain-text "typesetter" for TGN.

Output is "plain text" (i.e., UTF-8 with no markup) in the following format:

[<pretty-book-name> <chapter>:]<verse> - <verse-text-wrapped/align-indented>

The "text column" always starts at a fixed position on the page, with
reference text/numbers right-aligned to that point.

Book name/chapter number are printed only when transitioning chapter/book.
Non-contiguous verses are separated by a line of ". . ." characters in the text column.
"""
import argparse
import textwrap
from typing import IO, List

from ..data import VerseRef, BibleBooks
from ..ts import Typesetter

class Plaintext(Typesetter, name="plain"):
    def __init__(self, argv: List[str], bb: BibleBooks):
        ap = argparse.ArgumentParser(description="Fixed-column plain-text 'typesetter'")
        ap.add_argument("-m", "--max-column", type=int, default=100, 
                        help="Max width (in text columns) of output")
        ap.add_argument("-v", "--verse-column", type=int, default=None, 
                        help="Default text column for verse content (autocalculated by default)")
        args = ap.parse_args(argv)

        self._bb = bb 
        self._max_column = args.max_column
        if args.verse_column is not None:
            self._text_column = args.verse_column
        else:
            longest_n = -1
            longest_key = None
            for key, name in self._bb.pretty_names():
                if len(name) > longest_n:
                    longest_n = len(name)
                    longest_key = key
            self._text_column = len(self._format_full_ref(longest_key, 99, 999))
        self._last = VerseRef("n/a", 0, 0)

    def _format_full_ref(self, book, chapter, verse) -> str:
        pretty_name = self._bb.pretty_name(book)
        return f"{pretty_name} {chapter}:{verse} - "

    def _format_short_ref(self, verse) -> str:
        return f"{verse} - "

    def start(self, target_stream: IO):
        self._last = VerseRef("n/a", 0, 0)
        self._out = target_stream

    def debug(self, msg: str):
        print(msg, file=self._out)

    def feed(self, this: VerseRef, text: str):
        indent = ' '*self._text_column
        if self._bb.is_valid_ref(self._last) and not self._bb.refs_are_congituous(self._last, this):
            self._out.write(indent + ". . .\n")

        if this.chapter != self._last.chapter or this.book != self._last.book:
            leader = self._format_full_ref(this.book, this.chapter, this.verse)
        else:
            leader = self._format_short_ref(this.verse)
        
        body = textwrap.fill(text, width=self._max_column, initial_indent=indent, subsequent_indent=indent).lstrip()
        self._out.write(leader.rjust(self._text_column) + body + "\n")
        self._last = this

    def finish(self):
        self._out.flush()




