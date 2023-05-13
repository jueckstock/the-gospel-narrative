"""True typsetting with SILE output.

Unlike the Tex and HTML typesetters that were focused on highly-versified layouts,
the SILE typesetter produces an inline layout.  References are minimized and typeset
as grayed out small superscripts.

(BONUS: create a custom SILE document class/typesetter that can keep track of context
and automagically de-minimize the first reference of the page

* start: emits SILE prelude, including definitions for \\vref and \\gap
* debug: ignored
* feed: emits \\vref, \\gap, verse text, and \verse ... command sequence (possibly preceeded by a \discontinuity sequence)
* finish: emits SILE postlude and flushes output

Example:
--------

\\begin[papersize=statement]{document}
\\use[module=packages.color]
\\use[module=packages.raiselower]
\\font[size=10pt]

\\define[command=vref]{\\raise[height=4pt]{\\color[color=gray]{\\font[size=8pt]{\\process}}}}

\\define[command=gap]{ … }

\\vref{Gen 1:1}\\nobreak{}In the beginning God created the heaven and the earth.\\goodbreak
\\vref{2}\\nobreak{}And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.\\gap\\goodbreak
\\vref{3}\\nobreak{}And God said, Let there be light: and there was light.\\goodbreak

\\end{document}

"""
import argparse
import os
import re
import sys
from typing import IO, List, Optional

from ..data import VerseRef, BibleBooks
from ..ts import Typesetter


DEFAULT_PRELUDE_FILE = os.path.join(os.path.dirname(__file__), "default-sile-prelude.sil")

SILE_CHARS = re.compile(r"[%{}\\]")
SILE_REPLACEMENTS = {
    "%": "\\%",
    "{": "$\\{$",
    "}": "$\\}$",
    "\\": "$\\backslash$",
}


def silescape(verbatim: str) -> str:
    """Return <verbatim> escaped for inclusion into SILE source."""
    return SILE_CHARS.sub(lambda m: SILE_REPLACEMENTS[m.group(0)], verbatim)


class Sile(Typesetter, name="sile"):
    def __init__(self, argv: List[str], bb: BibleBooks):
        ap = argparse.ArgumentParser(description="Statement-size inline SILE typesetter")
        ap.add_argument("-p", "--prelude", type=str, default=DEFAULT_PRELUDE_FILE,
                        help="SILE prelude file defining \\vref and \\gap")
        args = ap.parse_args(argv)

        self._prelude_file = args.prelude

        self._bb = bb
        self._last = VerseRef("n/a", 0, 0)
        self._out = None
        self._para = False
    
    def start(self, target_stream: IO):
        self._out = target_stream
        with open(self._prelude_file, "rt", encoding="utf8") as fd:
            for line in fd:
                self._emit(line.rstrip())
    
    def _emit(self, text: str, end="\n"):
        if not self._out:
            raise RuntimeError("Cannot emit output before self.start(...)")
        print(text, file=self._out, end=end)

    def debug(self, msg: str):
        print(msg, file=sys.stderr) # no actuall inline debugging supported
    
    def paragraph(self):
        self._emit("\n") # produces double-EOL, paragraph break
        self._para = True

    def feed(self, this: VerseRef, text: str):
        if self._bb.is_valid_ref(self._last) and not self._bb.refs_are_congituous(self._last, this):
            if not self._para:
                self._emit("\\gap{}", end="")
            pretty_book = silescape(self._bb.pretty_name(this.book))
            self._emit(f"\\vref{{{pretty_book} {this.chapter}:{this.verse}}}", end="")
        else:
            self._emit(f"\\vref{{{this.verse}}}", end="")
        self._emit(f"\\nobreak{{}}{silescape(text)}\\goodbreak")
        self._last = this
        self._para = False
    
    def finish(self):
        self._emit("\\end{document}")
        self._out.flush()

