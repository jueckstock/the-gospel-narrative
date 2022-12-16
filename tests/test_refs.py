from .context import tgntools as tt

def gen_ref_seq(book: str, chapter: int, verse_range: range):
    for verse in verse_range:
        yield (book, chapter, verse)


def test_single_simple_refs(): 
    assert list(tt.parse_ref("Gen 1:27")) == [("Gen", 1, 27)]
    assert list(tt.parse_ref("Rom 8:28")) == [("Rom", 8, 28)]
    assert list(tt.parse_ref("Jde 1:3")) == [("Jde", 1, 3)]


def test_multi_simple_refs():
    assert list(tt.parse_ref("Gen 1:1;2:2")) == [("Gen", 1, 1), ("Gen", 2, 2)]
    assert list(tt.parse_ref("Gen 1:1 ; 2:2")) == [("Gen", 1, 1), ("Gen", 2, 2)]


def test_verse_ranges():
    assert list(tt.parse_ref("Gen 1:1-10")) == list(gen_ref_seq("Gen", 1, range(1, 11)))
    assert list(tt.parse_ref("Rom 8:26-39")) == list(gen_ref_seq("Rom", 8, range(26, 40)))
    assert list(tt.parse_ref("Gen 1:1-10;  6:2-9")) == (
        list(gen_ref_seq("Gen", 1, range(1, 11))) + 
        list(gen_ref_seq("Gen", 6, range(2, 10)))
    )


def test_single_compound_refs(): 
    assert list(tt.parse_ref("Gen 1:1-3:16")) == (
        list(gen_ref_seq("Gen", 1, range(1, 32))) +
        list(gen_ref_seq("Gen", 2, range(1, 26))) +
        list(gen_ref_seq("Gen", 3, range(1, 17)))
    )

def test_multi_compound_refs(): 
    assert list(tt.parse_ref("Gen 1:1-3:16; 3:17 - 4:4")) == (
        list(gen_ref_seq("Gen", 1, range(1, 32))) +
        list(gen_ref_seq("Gen", 2, range(1, 26))) +
        list(gen_ref_seq("Gen", 3, range(1, 25))) +
        list(gen_ref_seq("Gen", 4, range(1, 5)))
    )

def test_all():
    assert list(tt.parse_ref("Rom 7:24-8:5; 8:9,26-28,32-9:2")) == (
        list(gen_ref_seq("Rom", 7, range(24, 26))) + 
        list(gen_ref_seq("Rom", 8, range(1, 6))) + 
        [("Rom", 8, 9)] + 
        list(gen_ref_seq("Rom", 8, range(26, 29))) + 
        list(gen_ref_seq("Rom", 8, range(32, 40))) + 
        list(gen_ref_seq("Rom", 9, range(1, 3)))
    )
