import pygame, sys, threading
from pygame.locals import *
from vec2d import *
from math import sqrt, e, log
from random import uniform, gauss, sample
#import psyco
import networkx as nx

#single node
class node:
    def __init__(self, x):
        self.x        = x #position
        self.oldx     = x #old position
        self.a        = 0 #force accumulators

        self.marked   = False #for bfs
        self.color    = (int(uniform(0,150)), int(uniform(0,150)), int(uniform(0,150)))
        self.size     = int(uniform(5,30))
        self.weight   = self.size / 1.0
        self.numNodes = 0 #num of nodes this is connected to. filled in countNodes()

#single spring
class spring:
    def __init__(self, n1, n2, k = -60, restDist = 50):
        self.n1 = n1
        self.n2 = n2
        self.k = k
        self.rest = restDist

class Drawer(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        pygame.init()
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.screen.fill((0,0,0))

    def draw(self, nodes, springs):
        self.screen.fill((255,255,255))
        for n in nodes:
            pygame.draw.circle(self.screen, n.color, n.x.inttup(), n.size, 1)
        for s in springs:
            pygame.draw.line(self.screen, (0,0,0), s.n1.x.inttup(), s.n2.x.inttup(), 1)
        #for n in nodes:
            #v =  n.x - n.oldx
            #if v.length:
                #v.length = 30
                #v += n.oldx
            #pygame.draw.line(self.screen, (255,0,0), n.x.inttup(), v.inttup(), 1)
        pygame.display.flip()

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
        return vec2d(self.w/2, self.h /2)


class Graph(object):
    def __init__(self, world, n=20):
        self.world = world
        self.create_nodes(n)
        self.doBFS()
        self.doCount()

    def create_nodes(self, n):
        self.nodes   = []
        self.springs = []

        rpos = self.world.gen_random_pos(n, 10)
        for i, p in enumerate(rpos):
            z = node( p )
            if i == 0:
                z.x      = self.world.start_pos()
                z.weight = 3000
            self.nodes.append(z)

        for i, n in enumerate(self.nodes):
            nodes_before  = self.nodes[:i]
            if not nodes_before:
                continue
            nbr_ancestors = max(min(int(gauss(1,1)), len(nodes_before)), 1)
            ancestors     = sample(nodes_before, nbr_ancestors)
            for a in ancestors:
                s = spring(n, a)
                self.springs.append(s)

        self.G=nx.DiGraph()
        #self.G.add_nodes_from(self.nodes)
        for s in self.springs:
            self.G.add_edge(s.n1, s.n2)

    #do a BFS search to create the dictionary containing the length of the
    #shortest path between any two nodes in the graph, along springs
    def doBFS(self):
        #construct the initial dict
        self.paths={}
        for n in self.nodes:
            for n2 in self.nodes:
                if n == n2:
                    self.paths[(n,n2)] = 0
                else:
                    self.paths[(n,n2)] = 10 #10 if they arent connected

        #now run BFS on each node to find the right values and fill them in
        for n in self.nodes:
            lst=[n]
            d=1
            for n2 in self.nodes: #reset nodes
                n2.marked = False

            while len(lst) > 0:
                nn = lst[0]
                del lst[0]
                nn.marked = True

                for s in self.springs:
                    n2 = None
                    if s.n1 == nn:
                        n2 = s.n2
                    elif s.n2 == nn:
                        n2 = s.n1

                    if n2 != None and n2.marked == False:
                        #nn is part of this spring
                        #we found n2 in depth d from n
                        self.paths[(n,n2)] = min(d, self.paths[(n,n2)])
                        self.paths[(n2,n)]= min(d, self.paths[(n2,n)])
                        n2.color = nn.color

                        #append n2 to the lst
                        lst.append(n2)

                d+=1 #increment depth

    #count number of connections for each node
    #return the highest number of connections of any node
    def doCount(self):
        maxN = 0
        for n in self.nodes:
            k=0
            for s in self.springs:
                if s.n1 == n or s.n2 == n:
                    k+=1
            n.numNodes=k/2 #k/2 because graph is undirected. nodes are doublecounted
            if k/2 > maxN:
                maxN = k/2
        #now set the spring constants appropriately
        for s in self.springs:
            n=max(s.n1.numNodes, s.n2.numNodes)
            s.rest=100+n*20
        return maxN


#main class
class graphMain:
    def __init__(self):

        #psyco.full()
        self.world  = World(1024,1024)
        self.drawer = Drawer(self.world.w, self.world.h)

        #PHYSICS
        self.dt = 0.01 #time step
        self.friction = 0.05

        self.dragging = None #is user dragging a node?
        self.selected = None #selected node
        self.physics  = True #is physics enabled?

        self.c = 0 #program counter used in main loop

    #integrate one single time step to get new positions 
    #from old positions based on acceleration of each node.
    def verlet(self):
        for n in self.graph.nodes:
            temp = vec2d(n.x.x, n.x.y) #store old position
            #n.x += ((1.0 - self.friction)*n.weight*(n.x - n.oldx)) + n.a*self.dt*self.dt
            n.x += (((1.0 - self.friction)*(n.x - n.oldx)) + n.a + vec2d(-10,0))*self.dt*self.dt / n.weight
            n.oldx = temp

        for n in self.graph.nodes: #reset accelerations for next iteration
            n.a = 0.0

    #accumulate all the forces between all the nodes
    def accumulate_force(self):

        #REPELL NODES CLOSE TO OTHER NODES
        #proportional to their separation in graph
        #Nodes are close => big attraction
        #Nodes are far => no attraction
        for n1 in self.graph.nodes:
            for n2 in self.graph.nodes:
                d   = self.graph.paths[(n1,n2)]    #distance in graph btw n1 and n2
                dst = n1.x.get_distance(n2.x) -(n1.size + n2.size)#distance on actual layout
                #==
                if d == 0:
                    continue
                elif d == 1:
                    # attract
                    repulsive_force = max(0, (n1.size + n2.size) - dst) * 5 **2 
                    if repulsive_force:
                        dp = n2.x - n1.x #get vector from n1->n2
                        dp.length = repulsive_force #set its length to strength of interaction
                        n2.a += -dp #add that vector to both acceleration of n1 and n2
                        n1.a += +dp        
                else :
                    repulsive_force = max(0, (n1.size + n2.size) - dst) * 5 **2 * d**2
                    if repulsive_force:
                        dp = n2.x - n1.x #get vector from n1->n2
                        dp.length = repulsive_force #set its length to strength of interaction
                        n2.a += +dp #add that vector to both acceleration of n1 and n2
                        n1.a += -dp        
                #==
                #if d > 1 and  dst< 200:
                    #dp = n2.x - n1.x #get vector from n1->n2
                    #dp.length = 2000/d #set its length to strength of interaction
                    #n2.a += dp #add that vector to both acceleration of n1 and n2
                    #n1.a += -dp        

        #SPRING STUFF
        for s in self.graph.springs:
            dp = s.n2.x - s.n1.x #get vector pointing from n1->n2

            if dp.length != 0:
                dx = dp.length - s.rest #get the displacement from rest length
                dp.length = s.k*dx #multiply by spring contant
                s.n2.a += dp #add the vector to each n1 and n2 accelerations
                s.n1.a += -dp

    #return the net movement of all nodes.
    #if there is very little movement then the simulation
    #can be stopped and result returned
    def netMovement(self):
        a=0.0
        for n in self.graph.nodes:
            a+= (n.x - n.oldx).length
        return a

    #handle all user input and interactivity
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    #self.quit()
                    return False
                elif event.key == K_r:
                    self.graph = Graph(self.world)
                #elif event.key == K_d:
                    ##delete closest node
                    #d = self.findclosest(pygame.mouse.get_pos())
                    #toRem = []
                    #for s in self.graph.springs:
                        #if s.n1 == d or s.n2 == d:
                            #toRem.append(s)
                    #for t in toRem:
                        #self.graph.springs.remove(t)
                    #self.graph.nodes.remove(d)
                    #self.doBFS()
                    #self.doCount()
                elif event.key == K_p:
                    self.physics = not self.physics
                elif event.key == K_n:
                    for z in self.graph.nodes:
                        z.x = vec2d(uniform(self.w/2-10,self.w/2+10), uniform(self.h/2-10,self.h/2+10))
                        z.oldx = z.x

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = None
                else:
                    now = vec2d(event.pos)
                    then = vec2d(self.selected)
                    if now.get_distance(then) < 10:
                        #just make a new node here (at now)
                        self.graph.nodes.append(node(now))
                        self.graph.doBFS()
                        self.graph.doCount()
                    else:
                        #make new line btw last node and this node
                        nowNode=self.findclosest(now)
                        thenNode=self.findclosest(then)
                        self.graph.springs.append(spring(nowNode, thenNode))
                        self.graph.doBFS()
                        self.graph.doCount()

                    self.selected = None

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.dragging = self.findclosest(event.pos)
                else:
                    self.selected = event.pos
        return True

    #find the closest node to position p. p is a vec2d
    def findclosest(self, p):
        ld = self.world.w + self.world.h
        li = None
        v = vec2d(p)
        for n in self.graph.nodes:
            d = v.get_distance(n.x) 
            if d < ld:
                ld = d
                li = n
        return li

    #draw all springs and nodes
    def draw(self):
        self.drawer.draw(self.graph.nodes, self.graph.springs)
    #true if there is no spring yet between the k'th and l'th node
    def dnc(self, k, l):
        i=self.graph.nodes[k]
        j=self.graph.nodes[l]
        for s in self.graph.springs:
            if (s.n1==i and s.n2==j) or (s.n1==j and s.n2==i):
                return False
        return True

    #initialize all the nodes and springs
    def initNodes(self):
        self.c       = 0


    #main method. do the simulation
    def setup(self):
        self.graph = Graph(self.world)

    def run(self, physics=False):    
        while 1:

            self.c +=1

            #simulate until net movement is very low, but
            #at least for 100 time steps
            #also simulate if user is dragging a node
            nm = self.netMovement()
            if nm > -0.5 or self.c < 100 or self.dragging:
                #if physics is enabled then do simulation
                if physics: 
                    self.accumulate_force()
                    self.verlet()

            cont = self.handle_input() #handle all user input
            if not cont: return

            #handle node dragging
            if not self.dragging == None:
                pos = pygame.mouse.get_pos()
                self.dragging.x = vec2d(pos)
                self.dragging.oldx = vec2d(pos)

            #draw everything
            self.draw()

    def quit(self):
        pygame.quit()
        #sys.exit(1)

def main():
    s = graphMain()
    s.setup()
    #s.run()
    s.draw()
    return s

if __name__ == '__main__':
    main()
