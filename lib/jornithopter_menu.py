'''
File containing the menu mode code for jornithopter
'''

from __future__ import division

from pyglet import text
from pyglet.event import EVENT_HANDLED
from pyglet.event import EVENT_UNHANDLED
from pyglet.window import key

import mode

import config
from common import *
from constants import *

menu_label = text.Label("MENU", font_size=20)

class MenuMode(mode.Mode):
    name = "menu"

    def __init__(self):
        super(MenuMode, self).__init__()

    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.control.switch_handler("game")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

    def on_draw(self):
        self.window.clear()
        menu_label.draw()
        if DEBUG:
            debug_label.draw()


