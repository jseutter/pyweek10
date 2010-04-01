'''
File containing character classes
'''

from __future__ import division

import config
import pyglet
from common import *
from constants import *

class Character(object):
    ''' Character baseclass '''
    def __init__(self, parent):
        ''' parent = the mode.Mode instance where this lives '''
        self.parent = parent
        # aliases to common func
        self.cx = self.parent.cx
        self.cy = self.parent.cy
        self.cxy = self.parent.cxy
    def update_pos(self, dt, direction):
        '''
        dt = time passed since last update
        direction = LEFT or RIGHT or UP or LEFT | UP or RIGHT | UP
        '''
        pass
    def draw(self):
        pass

class Hero(Character):
    def __init__(self, *args, **kwargs):
        Character.__init__(self, *args, **kwargs)
        bf = 10
        box_width = int(config.width / bf)
        box_height = int(config.height / bf) 
        box_start = int(config.width/2) - box_width//2, int(config.height/2) - box_height//2
        self.x,self.y = box_start
        self.width = box_width
        self.height = box_height
        for k in 'ax', 'ay', 'vx', 'vy':
            setattr(self, k, 0)

    def update_pos(self, dt, dir):
        # this will be replaced by a call to the world with current x,y
        # to see if land or not. If/When we get a world instance
        is_land = LAND
        if self.y > 0:
            is_land = AIR
        (dx,dy),(self.vx,self.vy,self.ax,self.ay) = physical_delta(
            dt, dir, is_land, (self.vx, self.vy, self.ax, self.ay))
        self.x += dx
        self.y += dy
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > config.height:
            self.y = config.height - self.height
        if self.x > config.width:
            self.x = 0
        elif self.x < 0 - self.width:
            self.x = config.width

    def draw(self):
        ps = [
            (self.x, self.y),
            (self.x+self.width, self.y),
            (self.x+self.width, self.y+self.height),
            (self.x, self.y+self.height),
        ]
        cps = []
        for p in ps:
            cps += self.cxy(p)

        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON, ('v2i', cps))


def physical_delta(dt, dir, is_land, oldva):
    ''' calculates the x and y delta for a given obj using some physical rules
    dir = direction of travel
    is_land = is object travel on land or air
    oldva = tuple of old vx, vy, ax, ay
    '''
    #dt seems tiny, make it BIGGER
    dt = dt * 25
    # untar oldva
    vxp,vyp,axp,ayp = oldva

    # Force calc
    side_res = AIRFRIC
    down_force = 0
    if is_land:
        side_res += GROUNDFRIC
    else:
        down_force = MASS * GRAVITY
    side_force = 0
    if dir & LEFT or dir & RIGHT:
        side_force = SIDETHRUST - side_res
        if side_force < 0:
            side_force = 0
    x_force = side_force
    if dir & LEFT:
        x_force = -side_force
    up_force = 0
    if dir & UP:
        up_force += UPTHRUST
    y_force = up_force - down_force
    # use prev ax & ay to remove associated force so you get an
    # elastic/natural movement not abrubt (i.e. FIXME force computation)

    # Acceleration
    ax = x_force / MASS
    ay = y_force / MASS

    # Distance traveled
    vx = ax * dt
    vy = ay * dt
    dx = vxp*dt + vx*dt/2
    dy = vyp*dt + vy*dt/2

    if DEBUG:
        print 'd&oldav:', (dx,dy),(vx,vy,ax,ay)

    return (dx,dy),(vx,vy,ax,ay)
