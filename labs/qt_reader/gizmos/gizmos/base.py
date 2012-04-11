from direct.showbase.DirectObject import DirectObject


from pandac.PandaModules          import Point3, Vec3, Plane, NodePath
from direct.task.Task             import Task
from constants                    import *

class Base( NodePath, DirectObject ):

    def __init__( self, name, camera ):
        NodePath.__init__( self, name )
        DirectObject.__init__( self )
        self.name        = name
        self.camera      = camera
        self.__task      = None
        self.attachedNps = []
        self.dragging    = False
        self.local       = True
        self.planar      = False
        self.size        = 1
        self.axes        = []
        # Set this node up to be drawn over everything else
        self.setBin( 'fixed', 40 )
        self.setDepthTest( False )
        self.setDepthWrite( False )

    def __UpdateTask( self, task ):
        """
        Main update task used by the gizmo which is added and removed from the
        task manager whenever a gizmo is stopped and started. Provide
        additional behaviour by overriding the Update method.
        """
        # Increate gizmo side by distance to camera so it always appears the
        # same size
        scale = ( self.getPos() - self.camera.getPos() ).length() / 10
        self.setScale( scale )
        # Call transform if the mouse is down
        if self.dragging:
            self.Transform()
        # Perform any additional update tasks
        self.Update( task )
        return Task.cont

    def AcceptEvents( self ):
        """Bind all events for the gizmo."""
        self.accept( 'mouse1-up' , self.OnMouseUp )
        self.accept( 'mouse2-up' , self.OnMouseUp )
        self.accept( 'mouse2'    , self.OnMouse2Down )
        #==
        self.accept( '%s-mouse1'         %self.name, self.OnNodeMouse1Down, [False] )
        self.accept( '%s-control-mouse1' %self.name, self.OnNodeMouse1Down, [True] )
        self.accept( '%s-mouse-over'     %self.name, self.OnNodeMouseOver )
        self.accept( '%s-mouse-leave'    %self.name, self.OnNodeMouseLeave )

    def Start( self ):
        """
        Starts the gizmo adding the task to the task manager, refreshing it
        and deselecting all axes except the default one.
        """
        self.__task = taskMgr.add( self.__UpdateTask, ''.join( [self.name, 'UpdateTask'] ) )
        # Refresh the gizmo
        self.Refresh()
        # Select the default axis, deselect all others
        for axis in self.axes:
            if axis.default:
                axis.Select()
            else:
                axis.Deselect()
        # Accept events
        self.AcceptEvents()

    def Stop( self ):
        """
        Stops the gizmo by hiding it and removing it's update task from the
        task manager.
        """
        if self.__task is not None:
            taskMgr.remove( self.__task )
        # Hide the gizmo and ignore all events
        self.detachNode()
        self.ignoreAll()

    def Update( self, task ):
        """
        Override this method to provide the gizmo with any additional update
        behavior.
        """
        pass

    def Transform( self ):
        """
        Override this method to provide the gizmo with transform behavior.
        """
        pass

    def AttachNodePaths( self, nps ):
        """
        Attach node paths to the gizmo. This won't affect the node's position
        in the scene graph, but will transform the objects with the gizmo.
        """
        self.attachedNps = nps
        for p in self.attachedNps:
            assert_(p.getPythonTag( "mesh_view" ))

    def SetSize( self, factor ):
        """
        Used to scale the gizmo by a factor, usually by 2 (scale up) and 0.5
        (scale down). Set both the new size for the gizmo also call set size
        on all axes.
        """
        self.size *= factor
        # Each axis may have different rules on how to appear when scaled, so
        # call set size on each of them
        for axis in self.axes:
            axis.SetSize( self.size )

    def GetAxis( self, collEntry ):
        """
        Iterate over all axes of the gizmo, return the axis that owns the
        solid responsible for the collision.
        """
        node = collEntry.getIntoNode()
        print node 
        for axis in self.axes:
            if node in axis.collNodes:
                return axis
        # No match found, return None
        print axis.collNodes, "collNodes"
        return None

    def GetSelectedAxis( self ):
        """Return the selected axis of the gizmo."""
        for axis in self.axes:
            if axis.selected:
                return axis

    def ResetAxes( self ):
        """
        Reset the default colours and flag as unselected for all axes in the 
        gizmo.
        """
        for axis in self.axes:
            axis.Deselect()

    def Refresh( self ):
        """
        If the gizmo has node paths attached to it then move the gizmo into
        position, set its orientation and show it. Otherwise hide the gizmo.
        """
        if self.attachedNps:
            attachedNps = list(self.attachedNps)
            # Show the gizmo
            self.reparentTo( render )
            # Move the gizmo into position
            self.setPos( attachedNps[0].getPos() )
            # Only set the orientation of the gizmo if in local mode
            if self.local:
                self.setHpr( attachedNps[0].getHpr() )
            else:
                self.setHpr( render.getHpr() )
        else:
            # Hide the gizmo
            self.detachNode()

    def OnMouseUp( self ):
        """
        Set the dragging flag to false and reset the size of the gizmo on the
        mouse button is released.
        """
        self.dragging = False
        self.SetSize( 1 )

    def OnNodeMouseLeave( self):
        """
        Called when the mouse leaves the the collision object. Remove the
        highlight from any axes which aren't selected.
        """
        for axis in self.axes:
            if not axis.selected:
                axis.Unhighlight()

    def OnNodeMouse1Down( self, planar, collEntry ):
        print "OnNodeMouse1Down"
        self.planar   = planar
        self.dragging = True
        # Store the attached node path's transforms
        self.initNpXforms = [np.getTransform() for np in self.attachedNps]
        # Reset colours and deselect all axes, then get the one which the
        # mouse is over
        self.ResetAxes()
        axis = self.GetAxis( collEntry )
        if axis is not None:
            # Select it
            axis.Select()
            # Get the initial point where the mouse clicked the axis
            self.initMousePoint = self.GetAxisPoint( axis )
        else:
            print "empty axis"

    def OnMouse2Down( self ):
        """
        Continue transform operation if user is holding mouse2 but not over
        the gizmo.
        """
        axis = self.GetSelectedAxis()
        if axis is not None:
            self.dragging = True
            self.initNpXforms = [np.getTransform() for np in self.attachedNps]
            self.initMousePoint = self.GetAxisPoint( axis )

    def OnNodeMouseOver( self, collEntry ):
        """Highlights the different axes as the mouse passes over them."""
        # Don't change highlighting if in dragging mode
        if self.dragging:
            return
        # Remove highlight from all unselected axes
        for axis in self.axes:
            if not axis.selected:
                axis.Unhighlight()
        # Highlight the axis which the mouse is over
        axis = self.GetAxis( collEntry )
        if axis is not None:
            axis.Highlight()

    def GetAxisPoint( self, axis ):

        def __GetMousePlaneCollisionPoint( planeNormal ):
            """
            Return the collision point of a ray fired through the mouse and a
            plane with the specified normal.
            """
            # Fire a ray from the camera through the mouse 
            mp = base.mouseWatcherNode.getMouse()
            p1 = Point3()
            p2 = Point3()
            self.camera.node().getLens().extrude( mp, p1, p2 )
            p1 = render.getRelativePoint( self.camera, p1 )
            p2 = render.getRelativePoint( self.camera, p2 )
            # Get the point of intersection with a plane with the normal
            # specified
            p = Point3()
            Plane( planeNormal, self.getPos() ).intersectsLine( p, p1, p2 )
            return p

        def __ClosestPointToLine( c, a, b ):
            """Returns the closest point on line ab to input point c."""
            u = ( c[0] - a[0] ) * ( b[0] - a[0] ) + ( c[1] - a[1] ) * ( b[1] - a[1] ) + ( c[2] - a[2] ) * ( b[2] - a[2] )
            u = u / ( ( a - b ).length() * ( a - b ).length() )
            x = a[0] + u * ( b[0] - a[0] )
            y = a[1] + u * ( b[1] - a[1] )
            z = a[2] + u * ( b[2] - a[2] )
            return Point3(x, y, z)
        # Get the axis vector - by default this is the selected axis'
        # vector unless we need to use the camera's look vector
        if axis.vector == CAMERA_VECTOR:
            axisVector = render.getRelativeVector( self.camera, Vec3(0, -1, 0) )
        else:
            axisVector = render.getRelativeVector( self, axis.vector )
        # Get the transform plane's normal. If we're transforming in
        # planar mode use the axis vector as the plane normal, otherwise
        # get the normal of a plane along the selected axis
        if self.planar or axis.planar:
            return __GetMousePlaneCollisionPoint( axisVector )
        else:
            # Get the cross of the camera vector and the axis vector - a
            # vector of 0, 1, 0 in camera space is coming out of the lens
            camVector = render.getRelativeVector( self.camera, Vec3(0, 1, 0) )
            camAxisCross = camVector.cross( axisVector )
            # Cross this back with the axis to get a plane's normal
            planeNormal = camAxisCross.cross( axisVector )
            p = __GetMousePlaneCollisionPoint( planeNormal )
            return __ClosestPointToLine( p, self.getPos(), self.getPos() + axisVector )
