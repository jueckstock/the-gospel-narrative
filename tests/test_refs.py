from .context import tgntools as tt


def test_single_simple_refs(): 
    assert list(tt.parse_ref("Gen 1:27")) == [("Gen", 1, 27)]
    assert list(tt.parse_ref("Rom 8:28")) == [("Rom", 8, 28)]
    assert list(tt.parse_ref("Jde 1:3")) == [("Jde", 1, 3)]


def test_multi_simple_refs():
    assert list(tt.parse_ref("Gen 1:1;Exo 2:2")) == [("Gen", 1, 1), ("Exo", 2, 2)]
    assert list(tt.parse_ref("Gen 1:1 ; Exo 2:2")) == [("Gen", 1, 1), ("Exo", 2, 2)]


def test_verse_ranges():
    assert list(tt.parse_ref("Gen 1:1-10")) == [("Gen", 1, i) for i in range(1, 11)]
    assert list(tt.parse_ref("Rom 8:26-39")) == [("Rom", 8, i) for i in range(26, 40)]
    assert list(tt.parse_ref("Gen 1:1-10; Rom 8:26-39")) == (
        [("Gen", 1, i) for i in range(1, 11)] 
        + [("Rom", 8, i) for i in range(26, 40)])

