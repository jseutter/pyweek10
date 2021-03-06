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
        self.last_uptick = 0
        Character.__init__(self, *args, **kwargs)
        box_width = 50
        box_height = 50
        box_start = int(config.width/2) - box_width//2, int(config.height/2) - box_height//2
        self.x,self.y = box_start
        self.width = box_width
        self.height = box_height
        for k in 'ax', 'ay', 'vx', 'vy':
            setattr(self, k, 0)

    def update_pos(self, dt, dir):
        # this will be replaced by a call to the world with current x,y
        # to see if land or not. If/When we get a world instance
        is_land = self.parent.world.is_land((self.x, self.y), self.width)
        if DEBUG:
            print 'IS_LAND:', is_land == LAND
        (dx,dy),(self.vx,self.vy,self.ax,self.ay) = physical_delta(
            dt, dir, is_land, (self.vx, self.vy, self.ax, self.ay), 
            self.last_uptick, self.parent.current_tick)
        collide = self.parent.world.land_collide((self.x, self.y), (dx,dy), self.width)
        if collide is None:
            self.x += dx
            self.y += dy
        else:
            if DEBUG:
                print 'COLLIDE'
            self.x, self.y = collide
        if self.y + self.height > config.height:
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


def physical_delta(dt, dir, is_land, oldva, last_uptick, current_tick):
    ''' calculates the x and y delta for a given obj using some physical rules
    dir = direction of travel
    is_land = is object travel on land or air
    oldva = tuple of old vx, vy, ax, ay
    '''
    # dt seems tiny, make it BIGGER
    dt = dt * 25
    # untar oldva
    vxp,vyp,axp,ayp = oldva

    # Force calc
    side_res = AIRFRIC
    down_force = 0
    if is_land:
        side_res += GROUNDFRIC
        if vyp < 0:
            vyp = 0
    else:
        down_force = MASS * GRAVITY
    # Horizontal Force
    x_force = 0
    if vxp > 0:
        x_force = -side_res
    elif vxp < 0:
        x_force = side_res
    if dir & LEFT:
        x_force += -SIDETHRUST
    elif dir & RIGHT:
        x_force += SIDETHRUST

    # Vertical Force
    up_force = 0
    if dir & UP:
        # Scale the uptrust based on how long ago the 
        # key was pressed
        if DEBUG:
            print "current_tick: %i, last_uptick: %i" % (current_tick, last_uptick)
        modifier = 1.0 - min(UPTHRUST_DURATION, current_tick - last_uptick) / UPTHRUST_DURATION
        up_force += UPTHRUST * modifier
    y_force = up_force - down_force

    # Acceleration
    ax = x_force / MASS
    ay = y_force / MASS

    # New Velocity
    vx = vxp + ax * dt
    vy = vyp + ay * dt

    # Check to see if our resistance force will cause the item to move in an
    # opposit direction and stop it. (Semi HACK)
    if vxp !=0 and (vx / vxp < 0) and not (dir & LEFT or dir & RIGHT):
        # dir change due to non SIDETHRUST force
        vx = vxp = ax = 0

    # HACK: cap the velocity at a terminal velocity
    # Technically, terminal velocity should just happen
    # if the air resistance was a dynamicly growing number
    if vx > TERMINALVELOCITY:
        vx = TERMINALVELOCITY
    elif vx < -TERMINALVELOCITY:
        vx = -TERMINALVELOCITY
    if vy > TERMINALVELOCITY:
        vy = TERMINALVELOCITY
    elif vy < -TERMINALVELOCITY:
        vy = -TERMINALVELOCITY

    # calculate displacement
    dx = ((vxp+vx)*dt)/2
    dy = ((vyp+vy)*dt)/2

    if DEBUG:
        print 'd&oldav:', (dx,dy),(vx,vy,ax,ay)

    return (dx,dy),(vx,vy,ax,ay)
