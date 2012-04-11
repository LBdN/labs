from pandac.PandaModules import CollisionTraverser, CollisionHandlerQueue, BitMask32
from pandac.PandaModules import CollisionNode, CollisionRay
from pandac.PandaModules import Vec4
import object as p3d
import marquee
from ..gizmos.constants import AXIS_COLLISION_MASK


class MousePicker( p3d.Object ):
    """
    Class to represent a ray fired from the input camera lens using the mouse.
    """

    def __init__( self, name, camera=None, rootNp=None, fromCollideMask=None, pickTag=None, gizmos=None ):
        p3d.Object.__init__( self, name, camera, rootNp )
        self.fromCollideMask = fromCollideMask
        self.pickTag         = pickTag
        self.selection       = set([])
        self.node            = None
        self.np              = None
        self.collEntry       = None
        self.gizmos          = gizmos
        assert self.gizmos is not None
        # Create a marquee
        self.marquee = marquee.Marquee( '%sMarquee' % self.name )
        # Create collision ray
        self.pickerRay   = CollisionRay()
        # Create collision node
        pickerNode = CollisionNode( self.name )
        pickerNode.addSolid( self.pickerRay )
        pickerNode.setFromCollideMask( self.fromCollideMask )
        self.pickerNp = camera.attachNewNode( pickerNode )
        #pickerNp.setCollideMask(AXIS_COLLISION_MASK)
        self.collHandler = CollisionHandlerQueue()
        self.collTrav = CollisionTraverser()
        self.collTrav.showCollisions( render )
        self.collTrav.addCollider( self.pickerNp, self.collHandler )
        # Bind mouse button events
        eventNames = ['mouse1', 'control-mouse1', 'mouse1-up']
        for eventName in eventNames:
            self.accept( eventName, self.FireEvent, [eventName] )
        #==
        self.selectionCol = None

    def FireEvent( self, event ):
        # Send a message containing the node name and the event name, including
        # the collision entry as arguments
        print "FireEvent", event, self.node
        if self.node is not None:
            print self.np, self.np.getName()
            messenger.send( '%s-%s' % ( self.node.getName(), event ), [self.collEntry] )
        elif event in ('mouse1', 'control-mouse1'):
            self.StartSelection()
        elif event == 'mouse1-up':
            if self.marquee.started:
                self.StopSelection()

    def UpdateTask( self, task ):
        #self.collTrav.traverse( self.rootNp ) # Traverse the hierarchy and find collisions
        self.collTrav.traverse(render) # Traverse the hierarchy and find collisions
        if self.collHandler.getNumEntries():  # If we have hit something,
            self.collHandler.sortEntries()    # sort the hits so that the closest is first
            collEntry = self.collHandler.getEntry( 0 )
        else:
            collEntry = None
        self.set_node( collEntry)
        # updating the pickerRay
        if base.mouseWatcherNode.hasMouse():
            mp = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens( self.camera.node(), mp.getX(), mp.getY() )
        return task.cont
    
    def set_node(self, collEntry):
        #==
        if collEntry : new_node = collEntry.getIntoNode()
        else         : new_node = None
        #==
        if new_node == self.node :
            # ultra triky bit, even if the node is th same
            # the collision is not and it is used for the picking later on
            if collEntry : self.collEntry = collEntry 
            return
        #==
        if self.node is not None:
            messenger.send( '%s-mouse-leave' % self.node.getName())
            self.np.setColorScale( Vec4(1) )
            self.node = None
        #==
        if new_node is not None:
            self.collEntry = collEntry
            self.node      = new_node
            #==
            self.np = self.collEntry.getIntoNodePath().getParent()
            self.np.setColorScale( Vec4(1, 0, 0, 1) )
            print self.np , self.np.getName()
            messenger.send( '%s-mouse-enter' %self.node.getName(), [collEntry] )
            messenger.send( '%s-mouse-over'  %self.node.getName(), [collEntry] )

    def StartSelection( self, clearSelection=True ):
        print "StartSelection"
        # Reset selected node colours
        if self.selectionCol:
            self.selectionCol.replace_nodes([])
        #for i in self.selection:
            #i.setColorScale( Vec4(1) )
        self.marquee.Start()
        #==
        if clearSelection:
            self.selection = set([])

    def StopSelection( self ):
        print "StopSelection"
        # Stop the marquee
        self.marquee.Stop()
        nodes = set([])
        for node in self.rootNp.findAllMatches( '**' ):
            if self.marquee.IsPoint3Inside( self.camera, self.rootNp, node.getPos() ):
                #if self.pickTag is None or node.getTag( self.pickTag ):
                if node.getPythonTag('mesh_view'):
                    nodes.add( node )
        # Add any node which was under the mouse to the selection
        if self.collHandler.getNumEntries():
            collEntry = self.collHandler.getEntry( 0 )
            node = collEntry.getIntoNodePath().getParent()
            if node.getPythonTag('mesh_view'):
                nodes.add( node )
            #nodes.add( node )
        self.selection = nodes
        #==
        if self.selectionCol:
            self.selectionCol.replace_nodes(nodes)
        #for i in self.selection:
            #i.setColorScale( Vec4(1, 0, 0, 1) )
        #==
        self.gizmos.AttachNodePaths( self.selection )
        if self.gizmos.active is not None:
            # Refresh the active gizmo so it appears in the right place
            self.gizmos.active.Refresh()
