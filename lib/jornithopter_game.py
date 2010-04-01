'''
File containing the game mode for jornithopter
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


game_label = text.Label("GAME", font_size=20)


class GameMode(mode.Mode):
    name = "game"

    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.control.switch_handler("menu")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

    def on_draw(self):
        self.window.clear()
        game_label.draw()
        if DEBUG:
            debug_label.draw()
