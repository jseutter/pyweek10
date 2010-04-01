"""Common code shared between modules.

This module is intended to be imported with 'from ... import *' semantics and
provides an __all__ specification for this purpose.

"""

__all__ = ["debug_label"]

from pyglet import text

debug_label = text.Label("DEBUG", font_size=20, y=24)
