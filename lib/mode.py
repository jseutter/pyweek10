"""Interface object framework.

"""

from __future__ import division

from pyglet.window import key

import config
from common import *
from constants import *


#: Global directory of modes, updated automatically when modes are created.
mode_directory = {}

def get_handler(name, *args, **kwds):
    """Return a handler for the given mode name or None.

    Additional arguments are passed to the mode constructer.

    :Parameters:
        `name` : str
            The mode name to look for.

    """
    mode = mode_directory.get(name)
    if mode is not None:
        return mode(*args, **kwds)


class ModeMeta(type):
    """Metaclass for interface objects.

    Updates the mode directory when a new mode is created.

    """

    def __init__(self, *args, **kwds):
        """Construct a ModeMeta object.

        """
        super(ModeMeta, self).__init__(*args, **kwds)
        if self.name is None and None in mode_directory:
            raise AssertionError, "must override mode name in subclasses"
        elif self.name in mode_directory:
            raise AssertionError, "mode %r already exists" % self.name
        mode_directory[self.name] = self


class Mode(object):
    """Base class for interface objects.

    Modes have an update method that is called every tick and define event
    handlers for the window and controller. Handlers (instances of a mode) are
    automatically pushed onto the window and controller event stacks when they
    are switched to, if they want to receive other events (e.g. from the model)
    they must manage that themselves.

    """

    __metaclass__ = ModeMeta

    #: The name used to key the mode in the mode directory.
    name = None

    def __init__(self):
        """Construct a Mode object.

        """
        self.keys = key.KeyStateHandler()
        self.width_factor = 1
        self.height_factor = 1

    def _calc_width_height_factors(self):
        '''
        We will code for a given config.width and config.height (e.g. 800x600)
        and we will use factors to convert to that. Effect is on larger screens
        everything will zoom larger
        '''
        w,h = self.window.get_size()
        wp,hp = config.width,config.height
        self.width_factor = w/wp
        self.height_factor = h/hp

    def cx(self, x):
        ''' Used to convert an x-ordinate or a width '''
        return int(self.width_factor * x)

    def cy(self, y):
        ''' Used to convert an y-ordinate or a height '''
        return int(self.height_factor * y)

    def cxy(self, p):
        ''' Used to convert an (x,y) co-ordinate or a (width,height) '''
        x,y = p
        return self.cx(x), self.cy(y)

    def connect(self, control):
        """Respond to the connecting controller.

        :Parameters:
            `control` : Controller
                The connecting Controller object.

        """
        self.control = control
        self.window = control.window
        self.window.push_handlers(self.keys)
        self._calc_width_height_factors()

    def disconnect(self):
        """Respond to the disconnecting controller.

        """
        self.window.remove_handlers(self.keys)
        self.window = None
        self.control = None

    def tick(self):
        """Process a single tick.

        """

    def update(self, dt):
        """Update real time components.

        :Parameters:
            `dt` : float
                The actual time that has passed since the last tick.

        """
