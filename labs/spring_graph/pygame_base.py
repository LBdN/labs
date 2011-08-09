import pygame
from pygame.locals import *

class World(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def gen_random_pos(self, nbr, margin):
        for i in range(nbr):
            yield vec2d( uniform( self.w/2-margin, self.w/2+margin ), 
                         uniform( self.h/2-margin,self.h/2+margin ) ) 

    def start_pos(self):
        return vec2d(10, self.h /2)

    def center(self):
        return (self.w/2, self.h /2)

class Drawable(object):
    def draw(self, screen, offset=None):
        self._draw(screen, offset=offset)

class Dot(Drawable):
    def __init__(self, size, pos, color):
        self.size = size
        self.pos  = pos
        self.color= color

    def _draw(self, screen, offset=None):
        pygame.draw.circle(screen, self.color, self.pos, self.size, 1)

class Line(Drawable):
    def __init__(self, start, end, color, width=1):
        self.start = start
        self.end   = end
        self.color = color
        self.width = width

    def _draw(self, screen, offset=None):
        pygame.draw.line(self.screen, self.color, self.start, self.end, self.width)


class Drawer(object):
    def __init__(self, w, h):
        self.w          = w
        self.h          = h
        self.drawables  = []
        self.first_draw = True

    def draw(self):
        if self.first_draw:
            pygame.init()
            self.screen = pygame.display.set_mode((self.w, self.h))
            self.screen.fill((0,0,0))
            self.first_draw = False
        #==
        self.screen.fill((255,255,255))
        for d in self.drawables:
            d.draw(self.screen)
        pygame.display.flip()
        
class Main:
    def __init__(self):
        self.world  = World(1024,1024)
        self.drawer = Drawer(self.world.w, self.world.h)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
        return True
    
    def run(self):
        while 1:
            self.c +=1
            cont = self.handle_input() #handle all user input
            if not cont: return
            #draw everything
            self.drawer.draw(self.graph.nodes, self.graph.springs)
