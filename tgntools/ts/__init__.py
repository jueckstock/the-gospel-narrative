"""Typesetting sub-package.

Defines a standard interface and registry for named typesetter classes
"""
from __future__ import annotations
from typing import IO, List

from ..data import VerseRef, BibleBooks

# internal (but global) Typesetter registry
_TYPESETTER_REGISTRY = {}


class Typesetter:
    """Base class of all typesetters.  Subclasses must provide a keyword argument "name" for the CLI name.

    Provides a stub implementation of the method interface (ctor, start, debug, feed, finish)
    and handles automatic named registration of Typesetter sub-classes.

    It is expected that sub-classes will perform argparse-style parsing of the `argv` array they receive
    and will exit with helpful usage messages as appropriate.
    """
    def __init__(self, argv: List[str], bb: BibleBooks):
        raise NotImplementedError()

    @classmethod
    def __init_subclass__(klass, /, name: str):
        try:
            old_klass = _TYPESETTER_REGISTRY[name]
            old_klass_name = old_klass.__module__ + old_klass.__qualname__
            raise NameError(f"duplicate typesetter name '{name}' (already used for '{old_klass_name}'")
        except KeyError:
            _TYPESETTER_REGISTRY[name] = klass
    
    def start(self, stream: IO):
        """Begin typsetting, saving output to the given file stream.
        """
        raise NotImplementedError()

    def debug(self, msg: str):
        """Insert a debugging message to the document stream at this point.

        Called only if the global "--debug" option is turned on.
        """
        raise NotImplementedError()

    def feed(self, this: VerseRef, text: str):
        """Add another verse reference/text to the typeset document.
        """
        raise NotImplementedError()

    def finish(self):
        """Perform any end-of-document typesetting tasks.
        """
        raise NotImplementedError()

    @staticmethod
    def get_registered_names() -> List[str]:
        """Static method to get all available/registered typesetter names.
        """
        return list(_TYPESETTER_REGISTRY.keys())

    @staticmethod
    def new(name: str, argv: List[str], bb: BibleBooks) -> Typesetter:
        """Create and return the named typesetter (using the given CLI arguments, if needed).
        """
        return _TYPESETTER_REGISTRY[name](argv, bb)

class Raw(Typesetter, name="raw"):
    """Simply dump verse contents with no reference data or formatting.

    Useful for word-counting, etc.
    """
    def __init__(self, argv: List[str], bb: BibleBooks):
        # ctor is a no-op for us!
        pass

    def start(self, stream: IO):
        self._s = stream

    def debug(self, msg: str):
        print(msg, file=self._s)

    def feed(self, this: VerseRef, text: str):
        print(text, file=self._s)

    def finish(self):
        self._s.flush()

