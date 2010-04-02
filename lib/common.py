"""Common code shared between modules.

This module is intended to be imported with 'from ... import *' semantics and
provides an __all__ specification for this purpose.

"""

__all__ = [
    "debug_label",
    "LEFT", "RIGHT", "UP",
    "LAND", "AIR",
    "MASS", "UPTHRUST", "SIDETHRUST", "GROUNDFRIC", "AIRFRIC", "GRAVITY",
    "TERMINALVELOCITY", "UPTHRUST_DURATION"
]

from pyglet import text

debug_label = text.Label("DEBUG", font_size=20, y=24)

(
LEFT,
RIGHT,
UP,
) = [int(2**i) for i in range(3)]

AIR,LAND = 0,1

MASS        = 20    # kg (all travelling objects for now)
UPTHRUST    = 300   # kg * m/s**2 (or what u call a Newton)
UPTHRUST_DURATION   = 20 # Ticks until the upthrust is negated
SIDETHRUST  = 100   # kg * m/s**2
GROUNDFRIC  = 40    # kg * m/s**2
AIRFRIC     = 20    # kg * m/s**2
GRAVITY     = 9.80665 # m/s**2 accell due to grav

TERMINALVELOCITY    = 20 # m/s (the fastest anything can get)

