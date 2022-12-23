"""HTML5/CSS typesetter for TGN.

* start: adds boilerplate HTML head/body-start
* debug: inserts <pre class="tgn-debug">`msg`</pre> tag
* feed: inserts <div class="tgn-verse-number">`verse`</div><div class="tgn-verse-text">`text`</div> tags
    * if book/chapter changed from previous verse, inserts <div class="tgn-verse-chapter">`chapter`</div> and <div class="tgn-verse-book">`book`</div>
    * if non-contiguous with last verse, inserts <hr class="tgn-ellipsis" /> before all

"""
import argparse
import os
from typing import IO, List, Optional

from ..data import VerseRef, BibleBooks
from ..ts import Typesetter


DEFAULT_STYLE_FILE = os.path.join(os.path.dirname(__file__), "default-html5-styles.css")


class Html5(Typesetter, name="html5"):
    def __init__(self, argv: List[str], bb: BibleBooks):
        ap = argparse.ArgumentParser(description="HTML5 typesetter")
        ap.add_argument("-c", "--class-prefix", type=str, default="tgn",
                        help="Prefix of CSS class names generated")
        ap.add_argument("-s", "--style-sheet", type=str, default=DEFAULT_STYLE_FILE,
                        help="CSS file to paste into output HTML.")
        ap.add_argument("-i", "--inline-styles", type=bool, default=True,
                        help="Inject CSS into HTML instead of adding a stylesheet link")
        args = ap.parse_args(argv)

        self._bb = bb 
        self._prefix = args.class_prefix
        self._style_sheet_file = args.style_sheet
        self._inline_styles = args.inline_styles

        self._last = VerseRef("n/a", 0, 0)
        self._out = None
        self._indent = 0
        self._open_tags = []

    def _emit(self, line: str):
        if not self._out:
            raise RuntimeError("cannot emit HTML before .start(..)")
        print(" "*self._indent + line, file=self._out)

    def _tag(self, tag: str, contents: Optional[str], klass: Optional[str] = None):
        if klass:
            opener = f'<{tag} class="{self._prefix}-{klass}"'
        else:
            opener = f'<{tag}'

        if contents is not None:
            self._emit(f'{opener}>{contents}</{tag}>')
        else:
            self._emit(f'{opener} />')

    def _open(self, tag: str, klass: Optional[str] = None):
        if klass:
            self._emit(f'<{tag} class="{self._prefix}-{klass}">')
        else:
            self._emit(f'<{tag}>')
        self._open_tags.append(tag)
        self._indent += 4

    def _close(self):
        self._indent -= 4
        tag = self._open_tags.pop()
        self._emit(f'</{tag}>')

    def start(self, target_stream: IO):
        self._last = VerseRef("n/a", 0, 0)
        self._out = target_stream

        self._open("html")
        self._open("head")
        self._tag("title", "The Gospel Narrative")
        if self._inline_styles:
            self._open("style")
            with open(self._style_sheet_file, "rt", encoding="utf8") as fd:
                for line in fd:
                    self._emit(line.rstrip())
            self._close()
        else:
            self._emit(f'<link rel="stylesheet" href="{self._style_sheet_file}">')
        self._close()
        self._open("body")
        self._open("div", "content")

    def debug(self, msg: str):
        self._tag("pre", msg, "debug")

    def feed(self, this: VerseRef, text: str):
        if self._bb.is_valid_ref(self._last) and not self._bb.refs_are_congituous(self._last, this):
            self._tag("hr", None, "skip")

        self._open("div", "verse-box")
        self._tag("div", text, "verse-text")
        self._tag("div", this.verse, "verse-number")
        if this.chapter != self._last.chapter or this.book != self._last.book:
            self._tag("div", this.chapter, "verse-chapter")
            self._tag("div", self._bb.pretty_name(this.book), "verse-book")
        self._close()
        self._last = this

    def finish(self):
        while self._open_tags:
            self._close()
        self._out.flush()




