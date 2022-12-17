"""Executable CLI tool for generating narrative output from an edit list.
"""
import argparse
import sys

from .refs import parse_ref
from .data import BibleBooks


bb = BibleBooks.fromfile()

for line in sys.stdin:
    line = line.strip()
    if line.startswith("#"):
        continue
    for vr in parse_ref(line, bb):
        print(bb[vr])
    
