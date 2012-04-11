import math

from pandac.PandaModules import NodePath, LineSegs, Geom, GeomNode, GeomTriangles
from pandac.PandaModules import GeomVertexData, GeomVertexFormat, GeomVertexWriter
from pandac.PandaModules import Quat, Vec3,  Point2, Point3


def GetPointsForSquare( x, y, reverse=False ):
    points = []
    
    points.append( (0, 0) )
    points.append( (0, y) )
    points.append( (x, y) )
    points.append( (x, 0) )
    
    # Reverse the order if necessary
    if reverse:
        points.reverse()
        
    return points
    

def GetPointsForSquare2( x, y, reverse=False ):
    points = []
    
    points.append( Point2(0, 0) )
    points.append( Point2(0, y) )
    points.append( Point2(x, y) )
    points.append( Point2(x, 0) )
    
    # Reverse the order if necessary
    if reverse:
        points.reverse()
        
    return points
    

def GetPointsForBox( x, y, z ):
    points = []
    
    for dx in (0, x):
        for p in GetPointsForSquare( y, z, dx ):
            points.append( (dx, p[0], p[1] ) )
                          
    for dy in (0, y):
        for p in GetPointsForSquare( x, z, not dy ):
            points.append( (p[0], dy, p[1] ) )
                          
    for dz in (0, z):
        for p in GetPointsForSquare( x, y, dz ):
            points.append( (p[0], p[1], dz ) )
    
    return points
    

def GetPointsForArc( degrees, numSegs, reverse=False ):
    points = []
    
    radians = math.radians( degrees )
    for i in range( numSegs + 1 ):
        a = radians * i / numSegs
        y = math.sin( a )
        x = math.cos( a )
        
        points.append( (x, y) )
        
    # Reverse the order if necessary
    if reverse:
        points.reverse()
        
    return points
    

def RotatePoint3( p, v1, v2 ):
    v1.normalize()
    v2.normalize()
    cross = v1.cross( v2 )
    cross.normalize()
    if cross.length():
        a = v1.angleDeg( v2 )
        quat = Quat()
        quat.setFromAxisAngle( a, cross )
        p = quat.xform( p )
        
    return p
    

def GetGeomTriangle( v1, v2, v3 ):
    tri = GeomTriangles( Geom.UHDynamic )
    tri.addVertex( v1 )
    tri.addVertex( v2 )
    tri.addVertex( v3 )
    tri.closePrimitive()
    
    return tri
    

class Arc( NodePath ):
    
    """NodePath class representing a wire arc."""
    
    def __init__( self, radius=1.0, numSegs=16, degrees=360, axis=Vec3(1 , 0, 0),
                  thickness=1.0, origin=Point3(0, 0, 0) ):
        
        # Create line segments
        self.ls = LineSegs()
        self.ls.setThickness( thickness )
        
        # Get the points for an arc
        for p in GetPointsForArc( degrees, numSegs ):
            
            # Draw the point rotated around the desired axis
            p = Point3(p[0], p[1], 0) - origin
            p = RotatePoint3( p, Vec3(0, 0, 1), axis )
            self.ls.drawTo( p * radius )
        
        # Init the node path, wrapping the lines
        node = self.ls.create()
        NodePath.__init__( self, node )
        

class Square( NodePath ):
    
    """NodePath class representing a wire square."""
    
    def __init__( self, width=1, height=1, axis=Vec3(1, 0, 0), thickness=1.0, origin=Point3(0, 0, 0) ):
        
        # Create line segments
        self.ls = LineSegs()
        self.ls.setThickness( thickness )
        
        # Get the points for an arc
        points = GetPointsForSquare( width, height )
        points.append( points[0] )
        for p in points:
            
            # Draw the point rotated around the desired axis
            p = Point3(p[0], p[1], 0) - origin
            p = RotatePoint3( p, Vec3(0, 0, 1), axis )
            self.ls.drawTo( p )
        
        # Init the node path, wrapping the lines
        node = self.ls.create()
        NodePath.__init__( self, node )
        

class Cone( NodePath ):
    
    """NodePath class representing a polygonal cone."""
    
    def __init__( self, radius=1.0, height=1.0, numSegs=16,
                  degrees=360, axis=Vec3(0, 0, 1), origin=Point3(0, 0, 0) ):
        
        # Create vetex data format
        gvf = GeomVertexFormat.getV3n3()
        gvd = GeomVertexData( 'vertexData', gvf, Geom.UHStatic )
        
        # Create vetex writers for each type of data we are going to store
        gvwV = GeomVertexWriter( gvd, 'vertex' )
        gvwN = GeomVertexWriter( gvd, 'normal' )
        
        # Get the points for an arc
        points = GetPointsForArc( degrees, numSegs, True )
        for i in range( len( points ) - 1 ):
            
            # Rotate the points around the desired axis
            p1 = Point3(points[i][0], points[i][1], 0) * radius
            p1 = RotatePoint3( p1, Vec3(0, 0, 1), axis ) - origin
            p2 = Point3(points[i + 1][0], points[i + 1][1], 0) * radius
            p2 = RotatePoint3( p2, Vec3(0, 0, 1), axis ) - origin

            cross = ( p2 - axis ).cross( p1 - axis )
            cross.normalize()
            
            gvwV.addData3f( p1 )
            gvwV.addData3f( axis * height - origin )
            gvwV.addData3f( p2 )
            gvwN.addData3f( cross )
            gvwN.addData3f( cross )
            gvwN.addData3f( cross )
            
            # Base
            gvwV.addData3f( p2 )
            gvwV.addData3f( Point3(0, 0, 0) - origin )
            gvwV.addData3f( p1 )
            gvwN.addData3f( -axis )
            gvwN.addData3f( -axis )
            gvwN.addData3f( -axis )
            
        geom = Geom( gvd )
        for i in range( 0, gvwV.getWriteRow(), 3 ):
            
            # Create and add triangle
            geom.addPrimitive( GetGeomTriangle( i, i + 1, i + 2 ) )
        
        # Init the node path, wrapping the box
        geomNode = GeomNode( 'cone' )
        geomNode.addGeom( geom )
        NodePath.__init__( self, geomNode )
    

class Box( NodePath ):
    
    """NodePath class representing a polygonal box."""
    
    def __init__( self, width=1, depth=1, height=1, origin=Point3(0, 0, 0) ):
        
        # Create vetex data format
        gvf = GeomVertexFormat.getV3n3()
        gvd = GeomVertexData( 'vertexData', gvf, Geom.UHStatic )
        
        # Create vetex writers for each type of data we are going to store
        gvwV = GeomVertexWriter( gvd, 'vertex' )
        gvwN = GeomVertexWriter( gvd, 'normal' )
        
        # Write out all points
        for p in GetPointsForBox( width, depth, height ):
            gvwV.addData3f( Point3( p ) - origin )
        
        # Write out all the normals
        for n in ( (-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1) ):
            for i in range( 4 ):
                gvwN.addData3f( n )
        
        geom = Geom( gvd )
        for i in range( 0, gvwV.getWriteRow(), 4 ):
            
            # Create and add both triangles
            geom.addPrimitive( GetGeomTriangle( i, i + 1, i + 2 ) )
            geom.addPrimitive( GetGeomTriangle( i, i + 2, i + 3 ) )

        # Init the node path, wrapping the box
        geomNode = GeomNode( 'box' )
        geomNode.addGeom( geom )
        NodePath.__init__( self, geomNode )
        

class SelectionBox( NodePath ):
    
    def __init__( self, width=1, depth=1, height=1, thickness=1.0, origin=Point3(0, 0, 0) ):
        
        def __Get3dPoint( pt, origin, axis ):
            p = Point3(pt.x, pt.y, 0) - origin
            return RotatePoint3( p, Vec3(0, 0, 1), axis )
        
        # Create line segments
        self.ls = LineSegs()
        self.ls.setThickness( thickness )
        
        #axes = [Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, 1), Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, 1)]
        #origins = [origin, origin, origin, origin + Point3(0, 0, -1), origin + Point3(0, 0, -1), origin + Point3(0, 0, 1)]
        axes = [Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(-1, 0, 0), Vec3(0, -1, 0)]
        origins = [origin, origin, origin, origin]
        for m in range( len( axes ) ):
        
            # Get the points for square, append the first one to the end to
            # complete the square
            pts = GetPointsForSquare2( width, height )
            pts.append( pts[0] )
            for i in range( len( pts ) - 1 ):
                
                # Get the distance a third of the way along the edge
                dist = ( pts[i+1] - pts[i] ) / 3
                
                # Draw one square
                self.ls.moveTo( __Get3dPoint( pts[i], origins[m], axes[m] ) )
                self.ls.drawTo( __Get3dPoint( pts[i] + dist, origins[m], axes[m] ) )
                self.ls.moveTo( __Get3dPoint( pts[i] + dist + dist, origins[m], axes[m] ) )
                self.ls.drawTo( __Get3dPoint( pts[i+1], origins[m], axes[m] ) )
        
        # Init the node path, wrapping the lines
        node = self.ls.create()
        NodePath.__init__( self, node )
        
        
class Test( GeomNode ):
    
    def __init__( self, name ):
        GeomNode.__init__( self, name )
        
        ls = LineSegs()
        ls.setThickness( 5 )
        ls.drawTo( Point3( 0,0,0 ) )
        ls.drawTo( Point3( 100,100,100 ) )
        self.addGeomsFrom( ls.create() )
        
        print ls
        
        #foo = ls.create()
        #print foo
        #print type( foo )
        #render.attachNewNode( foo )
        #self.addGeom( Line( Vec3( 0,0,0 ), Vec3( 100,100,100 ), thickness=10.0 ) )
        

class Line( NodePath ):
    
    """NodePath class representing a simple line."""
    
    def __init__( self, start, end, thickness=1.0 ):
        
        # Create line segments
        ls = LineSegs()
        ls.setThickness( thickness )
        ls.drawTo( Point3( start ) )
        ls.drawTo( Point3( end ) )
        
        # Init the node path, wrapping the lines
        NodePath.__init__( self, ls.create() )