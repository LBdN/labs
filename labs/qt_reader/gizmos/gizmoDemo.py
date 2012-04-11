import random
#import direct.directbase.DirectStart
from direct.directtools.DirectGrid import DirectGrid, DirectObject
from pandac.PandaModules           import Vec4, Vec3, Vec2, DirectionalLight, GeomNode
from direct.task.Task              import Task
from . import p3d
from . import gizmos

from gizmos.constants import AXIS_COLLISION_MASK

PICK_TAG = 'pickable'


class GizmoDemo( DirectObject ):

    def __init__( self ):
        DirectObject.__init__( self )
        # Create mouse
        base.disableMouse()
        self.mouse = p3d.Mouse()
        # Create camera
        self.camera = p3d.Camera( pos=(-250, -250, 200), style=
                                  p3d.CAM_USE_DEFAULT | 
                                  p3d.CAM_VIEWPORT_AXES )
        self.camera.Start()
        # Create scene root node
        self.rootNp = render.attachNewNode( 'rootNode' )
        # Create gizmo manager
        self.gizmoMgr = gizmos.Manager( {
            'pos' : gizmos.Translation ( 'pos', self.camera ),
            'rot' : gizmos.Rotation    ( 'rot', self.camera ),
            'scl' : gizmos.Scale       ( 'scl', self.camera )
                            })
        # Create node picker
        self.nodePicker = p3d.MousePicker( 'mouse',
                                           self.camera,
                                           self.rootNp,
                                           fromCollideMask = AXIS_COLLISION_MASK,
                                           #pickTag         = PICK_TAG,
                                           gizmos          = self.gizmoMgr)
        self.nodePicker.Start()
        # Bind node picker events
        #self.accept( 'mouse1', self.StartSelection )
        #self.accept( 'mouse1-up', self.StopSelection )

        # Create gizmo manager mouse picker
        #self.gizmoPicker = p3d.MousePicker( 'mouse', self.camera )
        #self.gizmoPicker.Start()
        # Create some objects
        #grid = DirectGrid( parent=render, planeColor=(0.5, 0.5, 0.5, 0.5) )
        #for i in range( 20 ):
            #ball = loader.loadModel( 'smiley' )
            #ball.setTag( PICK_TAG, '1' )
            #ball.reparentTo( self.rootNp )
            #ball.setPos( random.randint( -30, 30 ) * 2, random.randint( -30, 30 ) * 2, random.randint( -30, 30 ) * 2 )
            #ball.setScale( 10, 10, 10 )
        # Create a light
        dlight = DirectionalLight('dlight')
        dlight.setColor( ( 1, 1, 1, 1 ) )
        dlnp = render.attachNewNode(dlight)
        dlnp.setHpr(0, 0, 0)
        render.setLight(dlnp)
        dlnp.reparentTo( self.camera )
        # Create tasks
        taskMgr.add( self.MouseTask, 'mouseTask' )
        #==
        self.loader = loader


    def load(self, path):
        obj = self.loader.loadModel(path)
        obj.reparentTo(self.rootNp)
        return obj

    #def StartSelection( self, clearSelection=True ):
        #"""
        #Start the marquee if there is no active gizmo or the currently active
        #gizmo is not in dragging mode.
        #"""
        #active_gizmo = self.gizmoMgr.get_active()
        #if active_gizmo is not None and active_gizmo.dragging :
            #return
        #print active_gizmo, 
        #if active_gizmo :
            #return
            #print active_gizmo.dragging, 
        #print"StartSelection"
        ## Reset selected node colours
        #for i in self.nodePicker.selection:
            #i.setColorScale( Vec4(1) )
        #self.nodePicker.StartSelection( clearSelection )

    def StopSelection( self ):
        """
        Stop the marquee and attach the selected node paths to the managed
        gizmos.
        """
        # Return if the marquee is not running
#        if not self.nodePicker.marquee.IsRunning():
            #return
        ## Stop the marquee
        #self.nodePicker.StopSelection()
        ## Set the colour of the selected objects
        #for i in self.nodePicker.selection:
            #i.setColorScale( Vec4(1, 0, 0, 1) )
        # Attach the selection to the gizmo manager
#        self.gizmoMgr.AttachNodePaths( self.nodePicker.selection )
        ## Get the active gizmo
        #active_gizmo = self.gizmoMgr.get_active()
        #if active_gizmo is not None:
            ## Refresh the active gizmo so it appears in the right place
            #active_gizmo.Refresh()

    def MouseTask( self, task ):
        """
        Task to control mouse events. Gets called every frame and will
        update the scene accordingly.
        """
        # Return if no mouse is found or alt not down
        if not self.mouse.in_window or not self.mouse.alt_down:
            return Task.cont
        # ORBIT - If left mouse down
        if self.mouse.buttons[0]:
            self.camera.Orbit( Vec2(self.mouse.dx / 5.0, self.mouse.dy / 5.0) )
        # DOLLY - If middle mouse down
        elif self.mouse.buttons[1]:
            self.camera.Move( Vec3(self.mouse.dx / 5.0, 0, -self.mouse.dy / 5.0) )
        # ZOOM - If right mouse down
        elif self.mouse.buttons[2]:
            self.camera.Move( Vec3(0, -self.mouse.dx / 5.0, 0) )
        return Task.cont

# Launch app if main
if __name__ == '__main__':
    app = GizmoDemo()
    run()
