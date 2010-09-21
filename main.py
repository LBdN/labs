# -*- coding: UTF-8 -*-


from PyQt4.QtCore        import *
from PyQt4.QtGui         import *

P3D_WIN_WIDTH  = 800
P3D_WIN_HEIGHT = 500

from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject   import *
from pandac.PandaModules import WindowProperties
from pandac.PandaModules import loadPrcFileData
from pandac.PandaModules            import *

from direct.task                    import Task
from direct.interval.IntervalGlobal import *
from math                           import *

import sys

#loadPrcFileData("", "fullscreen 1")
loadPrcFileData("", "window-title Bridge")
loadPrcFileData("", "window-type none")

import direct.directbase.DirectStart
#----------------------------------------------------------------------
# definitions for dynamic object creation
#----------------------------------------------------------------------

graphVertexFormat = GeomVertexFormat.getV3n3c4t2()

#put here any font you like
#labelFont = loader.loadFont('arial.ttf')
#labelFont.setPointSize(10)

#----------------------------------------------------------------------
# PyQt GUI (taken from dinoint's 'post)
#----------------------------------------------------------------------

class QTTest(QDialog):
   def __init__(self, pandaCallback, parent=None):
      super(QDialog, self).__init__(parent)
      self.setWindowTitle("Test")
      self.setGeometry(30,30,800,600)
      
      self.pandaContainer = QWidget(self)
      self.pandaContainer.setGeometry(0,0,P3D_WIN_WIDTH,P3D_WIN_HEIGHT)
        hellobutton = Qt.QPushButton("Say 'Hello world!'",None)
         
# And connect the action "sayHello" to the event "button has been clicked"
        a.connect(hellobutton, Qt.SIGNAL("clicked()"), sayHello)

      self.lineedit = QLineEdit("Proba ugnjezdenog prikaza...")
      
      layout = QVBoxLayout()
      layout.addWidget(self.pandaContainer)
      layout.addWidget(self.lineedit)
      layout.addWidget(self.lineedit)
      layout.addWidget(self.lineedit)
      
      self.setLayout(layout)
      
      # this basically creates an idle task
      timer =  QTimer(self)
      self.connect( timer, SIGNAL("timeout()"), pandaCallback )
      timer.start(0)

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

#----------------------------------------------------------------------
# main program
#----------------------------------------------------------------------

class World(DirectObject):
   def __init__(self):
      base.disableMouse()


      #events
      self.accept('escape', sys.exit)
      self.accept('+', self.ZoomIn)
      self.accept('+-repeat', self.ZoomIn)
      self.accept('-', self.ZoomOut)
      self.accept('--repeat', self.ZoomOut)
      self.accept('*', self.RotateCW)
      self.accept('*-repeat', self.RotateCW)
      self.accept('/', self.RotateCCW)
      self.accept('/-repeat', self.RotateCCW)
      self.accept('enter', self.Cycle)
      self.accept('0', self.ResetPos)
      self.accept('5', self.RotateZ)
      
      self.seq = 0
      
      #this doesn't work after embedding panda into pyqt, so it's commented
      #self.ResetPos()
      
   def ResetPos(self):
      if self.seq <> 0 and self.seq.isPlaying(): return
      base.disableMouse()
      base.camera.setPos(0,-15,0)
      base.camera.setHpr(0,0,0)
      self.cycle = -2
      self.Cycle()

   def move(self, lerp) :
      if self.seq <> 0 and self.seq.isPlaying(): 
          return
      self.seq = Sequence(lerp)
      self.seq.start()

   def ZoomIn(self):
      posLerp = LerpPosInterval(base.camera,0.3,VBase3(0,base.camera.getY()+1,0),blendType='easeInOut')
      self.move(posLerp)
      
   def ZoomOut(self):
      posLerp = LerpPosInterval(base.camera,0.3,VBase3(0,base.camera.getY()-1,0),blendType='easeInOut')
      self.move(posLerp)
      
   def RotateCW(self):
      hprLerp = LerpHprInterval(base.camera,0.6,VBase3(0,0,base.camera.getR()-45),blendType='easeInOut')
      self.move(hprLerp)
      
   def RotateZ(self):
      hprLerp = LerpHprInterval(self.data.nodePath,2,VBase3(self.data.nodePath.getH()+360,0,0),blendType='easeInOut')
      self.move(hprLerp)
      
   def RotateCCW(self):
      hprLerp = LerpHprInterval(base.camera,0.6,VBase3(0,0,base.camera.getR()+45),blendType='easeInOut')
      self.move(hprLerp)

   def Cycle(self):
      self.cycle = self.cycle + 1
      if self.cycle == len(self.data.graphs): self.cycle = -1
      for idx, i in enumerate(self.data.graphs):
         if self.cycle == -1 or self.cycle == idx:
            i.nodePathGraphLab.show()
         else:
            i.nodePathGraphLab.hide()
         
   def step(self):
      taskMgr.step()
   
   def bindToWindow(self, windowHandle):
      wp = WindowProperties().getDefault()
      wp.setOrigin(0,0)
      wp.setSize(P3D_WIN_WIDTH, P3D_WIN_HEIGHT)
      wp.setParentWindow(windowHandle)
      base.openDefaultWindow(props=wp)

if __name__ == '__main__':
   world = World()
   app  = QApplication(sys.argv)
   form = QTTest(world.step)
   world.bindToWindow(int(form.winId()))
   form.show()
   app.exec_()
