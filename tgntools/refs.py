'''Tools for parsing/expanding book/chapter/verse references.
'''
from collections import namedtuple
from typing import Iterable


Verse = namedtuple("Verse", ("book", "chapter", "verse"))


def parse_ref(ref: str) -> Iterable[Verse]:
    return []
