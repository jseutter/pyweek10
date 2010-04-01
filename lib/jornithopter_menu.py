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

class FlashingLabel(text.Label):
    '''
    a text label that will flash by skiping calls to draw depending on the time
    that passed.
    '''
    BLINKFACTOR=10
    def __init__(self, *args, **kwargs):
        self.time = 0
        self.visible = True
        self.blink_speed = 1 # default blink_speed
        if 'blink_speed' in kwargs:
            self.blink_speed = kwargs['blink_speed']
            del kwargs['blink_speed']
        if 'parent' in kwargs:
            self._parent = kwargs['parent']
            del kwargs['parent']
        text.Label.__init__(self, *args, **kwargs)
        self._x = self.x
        self._y = self.y
        self.inited = False

    def update(self, dt):
        dt = dt * 25 # speed up dt a bit
        self.time += dt
        if self.time > self.blink_speed * self.BLINKFACTOR:
            self.time = 0
            self.visible = not self.visible

    def draw(self, *args, **kwargs):
        if not self.inited:
            self.x,self.y = self._parent.cxy((self._x,self._y))
            self.inited = True
        if self.visible:
            text.Label.draw(self, *args, **kwargs)

class MenuMode(mode.Mode):
    name = "menu"

    def __init__(self):
        super(MenuMode, self).__init__()
        x = config.width/2
        y = config.height/2
        self.play_label = FlashingLabel("PRESS SPACE TO PLAY",
                parent=self, # an aditional option not passed to text.Label
                font_size=20,
                x=x, y=y, anchor_x='center', anchor_y='center')


    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.control.switch_handler("game")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

    def update(self, dt):
        self.play_label.update(dt)

    def on_draw(self):
        self.window.clear()
        menu_label.draw()
        self.play_label.draw()
        if DEBUG:
            debug_label.draw()



