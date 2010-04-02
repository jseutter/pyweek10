'''
File containing the game mode for jornithopter
'''

from __future__ import division

import pyglet
from pyglet import text
from pyglet.event import EVENT_HANDLED
from pyglet.event import EVENT_UNHANDLED
from pyglet.window import key

import mode

import config
from common import *
from constants import *

from jornithopter_characters import Hero
from jornithopter_world import World

game_label = text.Label("GAME", font_size=20)


class GameMode(mode.Mode):
    name = "game"

    def __init__(self):
        mode.Mode.__init__(self)
        self.characters = [Hero(self)]
        self.dir = 0 # initial keypress direction
        self.world = World(self)

    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.control.switch_handler("menu")
        elif sym == key.LEFT:
            self.dir = self.dir | LEFT
        elif sym == key.RIGHT:
            self.dir = self.dir | RIGHT
        elif sym == key.UP:
            self.dir = self.dir | UP
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

    def on_key_release(self, sym, mods):
        if sym == key.LEFT:
            self.dir = self.dir & ~LEFT
        elif sym == key.RIGHT:
            self.dir = self.dir & ~RIGHT
        elif sym == key.UP:
            self.dir = self.dir & ~UP
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

    def update(self, dt):
        for c in self.characters:
            c.update_pos(dt, self.dir)

    def on_draw(self):
        self.window.clear()
        self.world.draw()
        game_label.draw()
        for c in self.characters:
            c.draw()
        if DEBUG:
            debug_label.draw()
