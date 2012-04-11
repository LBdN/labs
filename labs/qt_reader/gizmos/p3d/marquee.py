from pandac.PandaModules import NodePath, CardMaker, LineSegs, Point2

#from labs.qt_reader.gizmos import p3d
#from .. import p3d
import object as p3d


TOLERANCE = 1e-3


class Marquee( NodePath, p3d.Object ):
    """Class representing a 2D marquee drawn by the mouse."""

    def __init__( self, name, colour=(1, 1, 1, .2) ):
        p3d.Object.__init__( self, name )

        # Create a card maker
        cm = CardMaker( self.name )
        cm.setFrame( 0, 1, 0, 1 )
        # Init the node path, wrapping the card maker to make a rectangle
        NodePath.__init__( self, cm.generate() )
        self.setColor( colour )
        self.setTransparency( 1 )
        self.reparentTo( render2d )
        self.hide()
        # Create the rectangle border
        ls = LineSegs()
        ls.moveTo( 0, 0, 0 )
        ls.drawTo( 1, 0, 0 )
        ls.drawTo( 1, 0, 1 )
        ls.drawTo( 0, 0, 1 )
        ls.drawTo( 0, 0, 0 )
        # Attach border to rectangle
        self.attachNewNode( ls.create() )
        #==
        self.started = False

    def UpdateTask( self, task ):
        """
        Called every frame to keep the marquee scaled to fit the region marked
        by the mouse's initial position and the current mouse position.
        """
        # Check for mouse first, in case the mouse is outside the Panda window
        if base.mouseWatcherNode.hasMouse():
            # Get the other marquee point and scale to fit
            pos = base.mouseWatcherNode.getMouse() - self.initMousePos
            self.setScale( pos[0] if pos[0] else TOLERANCE, 1, pos[1] if pos[1] else TOLERANCE )
        return task.cont

    def IsPoint3Inside( self, camera, rootNode, point3d ):
        """Test if the specified point3 lies within the marquee area."""
        # Convert the point to the 3-d space of the camera
        p3 = camera.getRelativePoint( rootNode, point3d )

        # Convert it through the lens to render2d coordinates
        p2 = Point2()
        if not camera.GetLens().project( p3, p2 ):
            return False
        # Test point is within bounds of the marquee
        min, max = self.getTightBounds()
        TOL = 0
        if ( p2.getX() +TOL > min.getX() and p2.getX() -TOL < max.getX() and 
             p2.getY() +TOL > min.getZ() and p2.getY() -TOL < max.getZ() ):
            return True
        return False

    def Start( self ):
        p3d.Object.Start( self )
        # Move the marquee to the mouse position and show it
        self.initMousePos = Point2( base.mouseWatcherNode.getMouse() )
        self.setPos( self.initMousePos[0], 1, self.initMousePos[1] )
        self.show()
        self.started = True

    def Stop( self ):
        p3d.Object.Stop( self )
        # Hide the marquee
        self.hide()
        self.started = False
