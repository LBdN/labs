graphVertexFormat = GeomVertexFormat.getV3n3c4t2()
#----------------------------------------------------------------------
# graph classes
#----------------------------------------------------------------------

#2D point
class GraphCoordinate2D(object):
   def __init__(self,cx=0,cy=0):
      self.x = cx
      self.y = cy

#one subgraph
class SubGraph(object):
   def __init__(self, gData, stripNo, parentNode, colGraph = VBase4(0,1,0,1), colAxes = VBase4(1,0,0,1), colStrip = VBase4(0,0,0,1), scale = 1, thickness = 2):
      self.axesPoints = []      #axes (GraphCoordinate2D)
      self.rotation = 0         #graph rotation (not needed?)

      st = gData.strips[stripNo]   #get strip data
      self.stri = st

      #graph dimensions
      xmin = st.data[0].x
      xmax = xmin
      ymin = st.data[0].y
      ymax = ymin
      for i in st.data:
         if xmin > i.x : xmin = i.x
         if xmax < i.x : xmax = i.x
         if ymin > i.y : ymin = i.y
         if ymax < i.y : ymax = i.y
      label1Y = ymin
      label2Y = ymax
      if ymin > 0 : ymin = 0
      if ymax < 0 : ymax = 1

      arH = 0.2            #arrow height
      arW = 0.1            #arrow width
      yscale = 1.4         #axes scale (relative to graph size)
      
      ymax = ymax * yscale
      ymin = ymin * yscale
      
      #axes definition
      self.axesPoints.append(GraphCoordinate2D(0,0))            #[0](0,0) for Y
      self.axesPoints.append(GraphCoordinate2D(0,ymax))         #[1]end of Y
      self.axesPoints.append(GraphCoordinate2D(-arW,ymax-arH))   #[2]arrow 1
      self.axesPoints.append(GraphCoordinate2D(arW,ymax-arH))      #[3]arrow 2
      self.axesPoints.append(GraphCoordinate2D(0,0))            #[4](0,0) for X (so it can be different color)
      self.axesPoints.append(GraphCoordinate2D(xmax,0))         #[5]end of X
      self.axesPoints.append(GraphCoordinate2D(0,ymin))         #[6](eventually needed) more Y
      self.axesPoints.append(GraphCoordinate2D(xmin,0))         #[7](eventually needed) more X
      
      self.vertexData = GeomVertexData('GraphData', graphVertexFormat, Geom.UHDynamic)
      
      graphWriterVertex = GeomVertexWriter(self.vertexData, 'vertex')
      graphWriterNormal = GeomVertexWriter(self.vertexData, 'normal')
      graphWriterColor = GeomVertexWriter(self.vertexData, 'color')
      graphWriterTexcoord = GeomVertexWriter(self.vertexData, 'texcoord')

      graphPrimitive = GeomLines(Geom.UHStatic)
      graphPrimitiveStrip = GeomLines(Geom.UHStatic)

      #axes points
      firstPoint = 0
      for i in self.axesPoints:
         graphWriterVertex.addData3f(i.x*scale,0,i.y*scale)   #XYZ
         graphWriterNormal.addData3f(0,0,1)   #XYZ
         if firstPoint in [4,5,7]:
            graphWriterColor.addData4f(colStrip)   #RGBA
         else:
            graphWriterColor.addData4f(colAxes)   #RGBA
         graphWriterTexcoord.addData2f(0,0)   #UV
         firstPoint = firstPoint + 1
   
      #graph points
      lastPoint = firstPoint
      for i in st.data:
         graphWriterVertex.addData3f(i.x*scale,0,i.y*scale)   #XYZ
         graphWriterNormal.addData3f(0,0,1)   #XYZ
         graphWriterColor.addData4f(colGraph)   #RGBA
         graphWriterTexcoord.addData2f(0,0)   #UV
         lastPoint = lastPoint + 1

      #axes lines
      graphPrimitive.addVertices(0,1)
      graphPrimitive.closePrimitive()
      graphPrimitive.addVertices(1,2)
      graphPrimitive.closePrimitive()
      graphPrimitive.addVertices(1,3)
      graphPrimitive.closePrimitive()
      if self.axesPoints[6].x <> 0 or self.axesPoints[6].y <> 0:
         graphPrimitive.addVertices(0,6)
         graphPrimitive.closePrimitive()
      graphPrimitiveStrip.addVertices(4,5)
      graphPrimitiveStrip.closePrimitive()
      if self.axesPoints[7].x <> 0 or self.axesPoints[7].y <> 0:
         graphPrimitiveStrip.addVertices(4,7)
         graphPrimitiveStrip.closePrimitive()
      
      #graph lines
      for i in range(firstPoint,lastPoint-1):
         graphPrimitive.addVertices(i,i+1)
         graphPrimitive.closePrimitive()

      #node generation
      graphGeom = Geom(self.vertexData)
      graphGeom.addPrimitive(graphPrimitive)
      self.node = GeomNode('GraphNode')
      self.node.addGeom(graphGeom)
      self.nodePathAll = parentNode.attachNewNode("Dummy")
      self.nodePathGraphLab = self.nodePathAll.attachNewNode("Dummy")
      self.nodePathGraph = self.nodePathGraphLab.attachNewNode(self.node)
      self.nodePathGraph.setRenderModeThickness(thickness)
      self.nodePathGraphLab.setY(-0.05)
      graphGeomStrip = Geom(self.vertexData)
      graphGeomStrip.addPrimitive(graphPrimitiveStrip)
      self.nodeStrip = GeomNode('GraphNode')
      self.nodeStrip.addGeom(graphGeomStrip)
      self.nodePathStrip = self.nodePathAll.attachNewNode(self.nodeStrip)
      self.nodePathStrip.setRenderModeThickness(thickness*2)
      
      #labels
      self.label1 = TextNode('label1')
      self.label1.setText(str(round(label1Y,2)))
      #self.label1.setFont(labelFont)
      self.label1NodePath = self.nodePathGraphLab.attachNewNode(self.label1)
      self.label1NodePath.setTwoSided(True)
      self.label1NodePath.setColor(colGraph)
      self.label1NodePath.setPos(-0.5,0,label1Y)
      self.label1NodePath.setScale(0.2)
      self.label2 = TextNode('label2')
      self.label2.setText(str(round(label2Y,2)))
      #self.label2.setFont(labelFont)
      self.label2NodePath = self.nodePathGraphLab.attachNewNode(self.label2)
      self.label2NodePath.setTwoSided(True)
      self.label2NodePath.setColor(colGraph)
      self.label2NodePath.setPos(-0.5,0,label2Y)
      self.label2NodePath.setScale(0.2)

      #rotating and positioning of graph
      a = gData.lines[st.p2].x - gData.lines[st.p1].x
      b = gData.lines[st.p2].y - gData.lines[st.p1].y
      angle = degrees(-atan2(b,a))
      self.nodePathAll.setR(angle)
      self.nodePathAll.setPos(gData.lines[st.p1].x-4,0,gData.lines[st.p1].y)
      
#data for one strip
class StripData(object):
   def __init__(self):
      self.p1 = 0      
      self.p2 = 0      
      self.data = []   

#data for all subgraphs
class GraphData(object):
   def __init__(self):
       self.lines    = []
       self.strips   = []
       self.graphs   = []
       self.scale    = 1
       self.node     = 0
       self.nodePath = 0
