"""Executable CLI tool for generating narrative output from an edit list.
"""
import argparse
import sys

from .refs import parse_ref
from .data import BibleBooks, BIBLE_FILE

ap = argparse.ArgumentParser(description="Parse and typeset an edit list.")
ap.add_argument("-b", "--bible-file", default=None, type=str,
                help="Bible verse database file.")
ap.add_argument("-d", "--debug", default=False, action="store_true",
                help="DEBUG MODE: show edit list lines and verse references.")
ap.add_argument("edit_list", type=str, metavar="EDITS_FILE", help="Reference edit list file.")
args = ap.parse_args()

bb = BibleBooks.fromfile(args.bible_file or BIBLE_FILE)

with open(args.edit_list, "rt", encoding="utf8") as fd:
    for i, line in enumerate(fd):
        line = line.strip()
        if args.debug:
            print(f"{args.edit_list}:{i+1}: {line}")
        if line.startswith("#"):
            continue
        for vr in parse_ref(line, bb):
            if args.debug:
                print(vr, end="\t")
            print(bb[vr])
        
