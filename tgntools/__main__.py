"""Executable CLI tool for generating narrative output from an edit list.
"""
import argparse
import sys
from typing import IO

from .refs import parse_ref
from .data import BibleBooks, BIBLE_FILE, VerseRef
from .ts import Typesetter
from .ts import txt, html, tex, sile  # trigger autoregistration of all available typesetters


ap = argparse.ArgumentParser(description="Parse and typeset an edit list.")
ap.add_argument("-b", "--bible-file", default=None, type=str,
                help="Bible verse database file.")
ap.add_argument("-d", "--debug", default=False, action="store_true",
                help="DEBUG MODE: show edit list lines and verse references.")
ap.add_argument("edit_list", type=str, metavar="EDITS_FILE", help="Reference edit list file.")
ap.add_argument("typesetter", choices=Typesetter.get_registered_names(), help="Use the named typsetter (which may take additional CLI args)")
args, extra_argv = ap.parse_known_args()

bb = BibleBooks.fromfile(args.bible_file or BIBLE_FILE)
tts = Typesetter.new(args.typesetter, extra_argv, bb)

tts.start(sys.stdout)
emitted_para_break = False
with open(args.edit_list, "rt", encoding="utf8") as fd:
    for i, line in enumerate(fd):
        line = line.strip()
        if args.debug:
            tts.debug(f"{args.edit_list}:{i+1}: {line}")
        if line.startswith("#"):
            continue

        emitted_verse = False
        for vr in parse_ref(line, bb):
            tts.feed(vr, bb[vr])
            emitted_verse = True
            emitted_para_break = False

        # emit a paragraph break if we encountered a non-comment, non-verse line
        # (but only once, until after we've seen more verses)
        if not emitted_verse:
            if not emitted_para_break:
                tts.paragraph()
                emitted_para_break = True

tts.finish()
