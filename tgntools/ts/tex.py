"""True typsetting with plain TeX output.

* start: emits TeX prelude (definitions for \verse and \discontinuity, etc.)
* debug: emits {\tt ...} line
* feed: emits \verse ... command sequence (possibly preceeded by a \discontinuity sequence)
* finish: emits \end and flushes output

Notes:
------

* use \leftskip <fixed amount> and \rightskip <flex glue amount} to place verse text at mid-page with ragged right edges (no rivers)
    * https://www.overleaf.com/learn/latex/Articles/How_to_change_paragraph_spacing_in_LaTeX#The_fundamentals:_parameter_commands_and_examples
* use \llap{\hbox ...} to place reference information to the left of verse paragraphs
    * see pages 30-31 of `TeX for the Impatient` (available via OpenLibrary at archive.org)

% define the indentation point for verse text
\newdimen\verseindent \verseindent = 12pc

\def\verse#1 #2:#3 #4{
\noindent \leftskip = \verseindent % \parskip = .5\baselineskip
\llap{\hbox to \verseindent{\hfil \bf #1 #2:\hbox to 2em{#3\hfil}}}%
#4\par}


\verse Genesis 1:1 {In the beginning God created the heaven and the earth.}
\verse Genesis 1:27 {So God created man in his own image, in the image of God created he him; male and female created he them.}
\verse {II Chronicles} 36:14 {Moreover all the chief of the priests, and the people, transgressed very much after all the abominations of the heathen; and polluted the house of the LORD which he had hallowed in Jerusalem.}
"""
import argparse
import os
import re
from typing import IO, List, Optional

from ..data import VerseRef, BibleBooks
from ..ts import Typesetter


DEFAULT_PRELUDE_FILE = os.path.join(os.path.dirname(__file__), "default-plaintex-prelude.tex")

TEX_CHARS = re.compile(r"[$#&%_^~{}\\]")
TEX_REPLACEMENTS = {
    "$": "\\$",
    "#": "\\#",
    "&": "\\&",
    "%": "\\%",
    "_": "\\_",
    "^": "\\^{ }",
    "~": "\\~{ }",
    "{": "$\\{$",
    "}": "$\\}$",
    "\\": "$\\backslash$",
}


def texscape(verbatim: str) -> str:
    """Return <verbatim> escaped for inclusion into TeX source."""
    return TEX_CHARS.sub(lambda m: TEX_REPLACEMENTS[m.group(0)], verbatim)


class PlainTeX(Typesetter, name="tex"):
    def __init__(self, argv: List[str], bb: BibleBooks):
        ap = argparse.ArgumentParser(description="Plain TeX typesetter")
        ap.add_argument("-p", "--prelude", type=str, default=DEFAULT_PRELUDE_FILE,
                        help="TeX prelude file defining \\verse and \\discontinuity")
        args = ap.parse_args(argv)

        self._prelude_file = args.prelude

        self._bb = bb
        self._last = VerseRef("n/a", 0, 0)
        self._out = None
    
    def start(self, target_stream: IO):
        self._out = target_stream
        with open(self._prelude_file, "rt", encoding="utf8") as fd:
            for line in fd:
                self._emit(line.rstrip())
    
    def _emit(self, text: str):
        if not self._out:
            raise RuntimeError("Cannot emit output before self.start(...)")
        print(text, file=self._out)

    def debug(self, msg: str):
        self._emit(f"\line{{\\tt {texscape(msg)}}}")

    def feed(self, this: VerseRef, text: str):
        if self._bb.is_valid_ref(self._last) and not self._bb.refs_are_congituous(self._last, this):
            self._emit("\discontinuity")
            csname = "\\hardverse"
        else:
            csname = "\\verse"
        pretty_book = texscape(self._bb.pretty_name(this.book))
        self._emit(f"{csname} {{{pretty_book}}} {this.chapter}:{this.verse} {{{text}}}")
        self._last = this
    
    def finish(self):
        self._emit("\\end")
        self._out.flush()

