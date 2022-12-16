'''Package-context hack for testing without installing.

Usage: begin each test module with a 'from .context import tgntools' line

Recommended by https://docs.python-guide.org/writing/structure/
'''
import os
import sys

# prepend the in-development copy of the package onto the Python import path
_tests_subdir = os.path.dirname(__file__)
_main_project_dir = os.path.join(_tests_subdir, "..")
sys.path.insert(0, os.path.abspath(_main_project_dir))

# Import the package (so it can be imported from this "context" module)
import tgntools

