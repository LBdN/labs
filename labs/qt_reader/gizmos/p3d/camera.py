import math
from direct.task.Task             import Task
from pandac.PandaModules          import Camera as PCamera, Vec3, Quat, NodePath, LineSegs, PerspectiveLens

CAM_USE_DEFAULT   = 1
CAM_DEFAULT_STYLE = 2
CAM_VIEWPORT_AXES = 4

class Camera( NodePath ):
    """Class representing a camera."""

    class Target( NodePath ):
        """Class representing the camera's point of interest."""

        def __init__( self, pos=Vec3( 0, 0, 0 ) ):
            NodePath.__init__( self, 'target' )
            self.defaultPos = pos

    class Axes( NodePath ):
        """Class representing the viewport camera axes."""

        def __Create( self, thickness, length ):
            # Build line segments
            ls = LineSegs()
            ls.setThickness( thickness )
            # X Axis - Red
            ls.setColor( 1.0, 0.0, 0.0, 1.0 )
            ls.moveTo( 0.0, 0.0, 0.0 )
            ls.drawTo( length, 0.0, 0.0 )
            # Y Axis - Green
            ls.setColor( 0.0, 1.0, 0.0, 1.0 )
            ls.moveTo( 0.0,0.0,0.0 )
            ls.drawTo( 0.0, length, 0.0 )
            # Z Axis - Blue
            ls.setColor( 0.0, 0.0, 1.0, 1.0 )
            ls.moveTo( 0.0,0.0,0.0 )
            ls.drawTo( 0.0, 0.0, length )
            return ls.create()

        def __init__( self, thickness=1, length=25 ):
            ls = self.__Create( thickness, length )
            NodePath.__init__( self, ls )

    def __init__( self, 
                  name='camera', 
                  pos=Vec3( 0, 0, 0 ), 
                  targetPos=Vec3( 0, 0, 0 ),
                  style=CAM_DEFAULT_STYLE ):
        self.zoomLevel = 2
        self.defaultPos = pos
        self.style = style
        # Use Panda's default camera
        if self.style & CAM_USE_DEFAULT:
            self.cam = getBase().cam
            #self.camNode = getBase().camNode
        # Otherwise create a new one
        else:
            # Create camera
            self.cam = NodePath( PCamera( name ) )
            # Create lens
            lens = PerspectiveLens()
            lens.setAspectRatio( 800.0 / 300.0 )
            self.cam.node().setLens( lens )
        # Wrap the camera in this node path class
        NodePath.__init__( self, self.cam )
        # Create camera styles
        if self.style & CAM_VIEWPORT_AXES:
            self.axes = self.Axes()
            self.axes.reparentTo( pixel2d )
        # Create camera target
        self.target = self.Target( pos=targetPos )
        self.Reset()

    def Reset( self ):
        # Reset camera and target back to default positions
        self.target.setPos( self.target.defaultPos )
        self.setPos( self.defaultPos )
        # Set camera to look at target
        self.lookAt( self.target.getPos() )
        self.target.setQuat( self.getQuat() )

    def Move( self, moveVec ):
        # Modify the move vector by the distance to the target, so the further
        # away the camera is the faster it moves
        cameraVec = self.getPos() - self.target.getPos()
        cameraDist = cameraVec.length()
        moveVec *= cameraDist / 300
        # Move the camera
        self.setPos( self, moveVec )
        # Move the target so it stays with the camera
        self.target.setQuat( self.getQuat() )
        test = Vec3( moveVec.getX(), 0, moveVec.getZ() )
        self.target.setPos( self.target, test )

    def Orbit( self, delta ):
        # Get new hpr
        newHpr = Vec3()
        newHpr.setX( self.getH() + delta.getX() )
        newHpr.setY( self.getP() + delta.getY() )
        newHpr.setZ( self.getR() )
        # Set camera to new hpr
        self.setHpr( newHpr )
        # Get the H and P in radians
        radX = newHpr.getX() * ( math.pi / 180.0 )
        radY = newHpr.getY() * ( math.pi / 180.0 )
        # Get distance from camera to target
        cameraVec = self.getPos() - self.target.getPos()
        cameraDist = cameraVec.length()
        # Get new camera pos
        newPos = Vec3()
        newPos.setX( cameraDist * math.sin( radX ) * math.cos( radY ) )
        newPos.setY( -cameraDist * math.cos( radX ) * math.cos( radY ) )
        newPos.setZ( -cameraDist * math.sin( radY ) )
        newPos += self.target.getPos()
        # Set camera to new pos
        self.setPos( newPos )

    def cameraMovement( self, task ):
        x,y,z = self.cube.getPos()
        #smoothly follow the cube...
        self.setX( self.getX() - ( ( self.getX() - x - 18 * self.zoomLevel ) * 5 * globalClock.getDt() ) )
        self.setY( self.getY() - ( ( self.getY() - y + 5 * self.zoomLevel ) * 5 * globalClock.getDt() ) )
        self.setZ( 15 * self.ZOOMLEVEL )
        self.setHpr( 75, -37, 0 )
        return Task.cont

    def AxesTask( self, task ):
        # Position axes 30 pixels from bottom left corner
        #posY = 100# self.GetSize()[1]
        self.axes.setPos( Vec3( 30, 0, -30 ) )
        # Set rotation to inverse of camera rotation
        cameraQuat = Quat( self.getQuat() )
        cameraQuat.invertInPlace()
        self.axes.setQuat( cameraQuat )
        return Task.cont

    def Start( self ):
        if self.style & CAM_VIEWPORT_AXES:
            taskMgr.add( self.AxesTask, 'cameraAxesTask' )

    def Stop( self ):
        taskMgr.remove( self.Task )

    def GetLens( self ):
        return self.cam.node().getLens()
