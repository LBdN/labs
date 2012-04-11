from direct.showbase.DirectObject import DirectObject
from direct.task.Task             import Task

MOUSE_ALT = 0

class Mouse( DirectObject ):
    """Class representing the mouse."""

    def __init__( self ):
        DirectObject.__init__( self )
        #==
        self.x         = 0
        self.y         = 0
        self.dx        = 0
        self.dy        = 0
        #==
        self.buttons   = [False, False, False]
        self.stopped   = False
        self.alt_down  = False
        self.in_window = False
        # Bind button events
        self.accept( 'mouse1'     , self.set_state, [0, True] )
        self.accept( 'alt-mouse1' , self.set_state, [0, True, [MOUSE_ALT]] )
        self.accept( 'mouse1-up'  , self.set_state, [0, False, []] )
        self.accept( 'alt-mouse2' , self.set_state, [1, True, [MOUSE_ALT]] )
        self.accept( 'mouse2'     , self.set_state, [1, True] )
        self.accept( 'mouse2-up'  , self.set_state, [1, False, []] )
        self.accept( 'alt-mouse3' , self.set_state, [2, True, [MOUSE_ALT]] )
        self.accept( 'mouse3'     , self.set_state, [2, True] )
        self.accept( 'mouse3-up'  , self.set_state, [2, False, []] )
        #==
        taskMgr.add( self.update, 'mouseUpdate' )

    def set_state( self, id, value, modifiers=[] ):
        # Record buttons and modifiers
        self.buttons[id] = value
        self.alt_down    = MOUSE_ALT in modifiers

    def update( self, task ):
        # Get pointer from screen, calculate delta
        #==
        if self.stopped:
            return Task.done
        #==
        mp = getBase().win.getPointer( 0 )
        self.dx = self.x - mp.getX()
        self.dy = self.y - mp.getY()
        self.x  = mp.getX()
        self.y  = mp.getY()
        #==
        self.in_window = base.mouseWatcherNode.hasMouse()
        #==
        return Task.cont
