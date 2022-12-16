from .context import tgntools as tt

def test_parse_verse_line():
    v = tt.parse_verse_line("Gen|1|1| In the beginning God created the heaven and the earth.~\n")
    assert v.book == "Gen"
    assert v.chapter == 1
    assert v.verse == 1
    assert v.text == "In the beginning God created the heaven and the earth."

def test_book_limits():
    bb = tt.BibleBooks.fromfile()
    assert bb.last_chapter("Gen") == 50
    assert bb.last_verse("Gen", 1) == 31
