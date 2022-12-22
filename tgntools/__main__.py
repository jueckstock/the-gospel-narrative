"""Executable CLI tool for generating narrative output from an edit list.
"""
import argparse
import sys
from typing import IO

from .refs import parse_ref
from .data import BibleBooks, BIBLE_FILE, VerseRef
from .ts.txt import Plaintext


ap = argparse.ArgumentParser(description="Parse and typeset an edit list.")
ap.add_argument("-b", "--bible-file", default=None, type=str,
                help="Bible verse database file.")
ap.add_argument("-d", "--debug", default=False, action="store_true",
                help="DEBUG MODE: show edit list lines and verse references.")
ap.add_argument("-r", "--raw", default=False, action="store_true",
                help="RAW MODE: skip typesetting, just print verse text only.")
ap.add_argument("edit_list", type=str, metavar="EDITS_FILE", help="Reference edit list file.")
args = ap.parse_args()

bb = BibleBooks.fromfile(args.bible_file or BIBLE_FILE)


class RawMode:
    def start(self, stream: IO):
        self._s = stream

    def feed(self, this: VerseRef, text: str):
        print(text, file=self._s)

    def finish(self):
        self._s.flush()


if args.raw:
    tts = RawMode()
else:
    tts = Plaintext(100, 20, bb)

tts.start(sys.stdout)
with open(args.edit_list, "rt", encoding="utf8") as fd:
    for i, line in enumerate(fd):
        line = line.strip()
        if args.debug:
            print(f"{args.edit_list}:{i+1}: {line}")
        if line.startswith("#"):
            continue
        for vr in parse_ref(line, bb):
            tts.feed(vr, bb[vr])

tts.finish()
