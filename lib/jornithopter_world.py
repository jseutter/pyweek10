import pyglet
import config
from common import *

class World(object):
    def __init__(self, parent):
        self.parent = parent
        # aliases to common func
        for k in 'cx','cy','cxy':
            setattr(self, k, getattr(self.parent, k))
        # world stuff
        # island width and height
        self.positions = [
            # ( x, y, width, height )
            (50, 450, 250, 20),
            (500, 450, 150, 20),
            (100, 150, 150, 20),
            (450, 150, 250, 20),
            (250, 300, 300, 15),
        ]

    def is_land(self, p, w):
        '''
        Given a point p = (x,y) check if it is LAND or AIR
        w = obj width, p is anchor bottom left
        '''
        print p,
        x,y = p
        if y <= 0: # easy one it is land
            print 'MAIN'
            return LAND
        for xp,yp,lw,lh in self.positions:
            if xp-w <= x <= xp + lw and yp+lh == y:
                print 'X',xp,yp
                return LAND
        print 'AIR'
        return AIR

    def land_collide(self, p, dp, w):
        '''
        given point p and displacement dp return a landing point
        w = obj width, p is anchor bottom left
        '''
        print 'ctest:', p, dp
        x,y = p
        dx, dy = dp
        # easy one, main ground
        print y, y+dy, y>=0 and y+dy <= 0
        if y>=0 and y+dy <= 0:
            yn = 0
            ndx = dx*(yn-y)/dy if dy != 0 else dx
            xn = x + ndx 
            return (xn,yn)
        else:
            for xp,yp,lw,lh in self.positions:
                yp = yp + lh
                if y >= yp and y+dy <= yp:
                    ndx = dx*(yp-y)/dy if dy != 0 else dx
                    xn = x + ndx
                    if xp-w <= xn <= xp + lw:
                        return (xn, yp)
        return None


    def draw(self):
        for x,y,lw,lh in self.positions: # islands
            ps = [
                (x, y),
                (x+lw, y),
                (x+lw, y+lh),
                (x, y+lh),
            ]
            cps = []
            for p in ps:
                cps += self.cxy(p)

            pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON, ('v2i', cps))
