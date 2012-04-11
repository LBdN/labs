from pandac.PandaModules import Mat4, Vec3, Point3
from pandac.PandaModules import CollisionTube, CollisionSphere
from ..p3d import commonUtils
from ..p3d.geometry import Cone, Square, Line
from axis import Axis
from base import Base
from constants import *


class Translation( Base ):

    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        # Create x, y, z and camera normal axes
        self.axes.append( self.CreateArrow( Vec3(1, 0, 0), RED ) )
        self.axes.append( self.CreateArrow( Vec3(0, 1, 0), GREEN ) )
        self.axes.append( self.CreateArrow( Vec3(0, 0, 1), BLUE ) )
        self.axes.append( self.CreateSquare( Vec3(0, 0, 0), TEAL ) )

    def CreateArrow( self, vector, colour ):
        # Create the geometry and collision
        line = Line( (0, 0, 0), vector )
        cone = Cone( 0.05, 0.25, axis=vector, origin=vector * 0.25 )
        collTube = CollisionTube( (0,0,0), Point3( vector ) * 0.95, 0.05 )
        # Create the axis, add the geometry and collision
        axis = Axis( self.name, vector, colour )
        axis.AddGeometry( line, sizeStyle=SCALE )
        axis.AddGeometry( cone, vector, colour )
        axis.AddCollisionSolid( collTube, sizeStyle=TRANSLATE_POINT_B )
        axis.reparentTo( self )
        return axis

    def CreateSquare( self, vector, colour ):
        # Create the geometry and collision
        self.square = Square( 0.2, 0.2, Vec3(0, 1, 0), origin=Point3(0.1, 0.1, 0) )
        self.square.setBillboardPointEye()
        collSphere = CollisionSphere( 0, 0.125 )
        # Create the axis, add the geometry and collision
        axis = Axis( self.name, CAMERA_VECTOR, colour, planar=True, default=True )
        axis.AddGeometry( self.square, sizeStyle=NONE )
        axis.AddCollisionSolid( collSphere, sizeStyle=NONE )
        axis.reparentTo( self )
        return axis

    def Transform( self ):
        print "Transform"
        # Get the point where the mouse clicked the axis
        axis = self.GetSelectedAxis()
        axisPoint = self.GetAxisPoint( axis )
        # Get the gizmo's translation matrix and transform it
        trans_vector =  self.initXform.getPos() - self.getPos() + axisPoint - self.initMousePoint 
        newTransMat = Mat4().translateMat(trans_vector)
        self.setMat( self.getMat() * newTransMat )
        # Get the attached node path's translation matrix
        transVec = axisPoint - self.initMousePoint
        if axis.vector != CAMERA_VECTOR:
            transVec = self.getRelativeVector( render, transVec ) * self.getScale()[0]
        newTransMat = Mat4().translateMat( transVec )
        # Transform attached node paths
        print self.attachedNps
        for i, np in enumerate( self.attachedNps ):
            # Perform transforms in local or world space
            if self.local and axis.vector != CAMERA_VECTOR:
                transMat, rotMat, scaleMat = commonUtils.GetTrsMatrices( self.initNpXforms[i] )
                new_mat = scaleMat * newTransMat * rotMat * transMat
            else:
                new_mat = self.initNpXforms[i].getMat() * newTransMat 
            po=  np.getPythonTag('mesh_view')
            if po:
                po.translate(trans_vector)
            else:
                print "no po %s:%s" %(np, type(np))
                np.setMat(  new_mat)

    def OnNodeMouse1Down( self, planar, collEntry ):
        Base.OnNodeMouse1Down( self, planar, collEntry )
        # Store the gizmo's initial transform
        self.initXform = self.getTransform()
        # If in planar mode, clear the billboard effect on the center square
        # and make it face the selected axis
        axis = self.GetSelectedAxis()
        if self.planar and not axis.planar:
            self.square.clearBillboard()
            self.square.lookAt( self, Point3( axis.vector ) )
        else:
            self.square.setHpr( Vec3(0, 0, 0) )
            self.square.setBillboardPointEye()

    def OnMouse2Down( self ):
        Base.OnMouse2Down( self )
        # Store the gizmo's initial transform
        self.initXform = self.getTransform()
