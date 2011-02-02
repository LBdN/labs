# -*- coding: utf-8 -*-
  
"""
Module implementing MainWindow.
"""
from PyQt4        import QtCore, QtGui
from PyQt4.QtGui  import QMainWindow
from PyQt4.QtCore import pyqtSignature
#from Ui_neteditor import Ui_MainWindow
#from data_io      import loadData
from numpy        import array
#==
#import networkx as nx
import math
#import elasticnodes as dgraph

class GraphWidget(QtGui.QGraphicsView):
    def __init__(self):
        super(GraphWidget, self).__init__()

        #self.timerId = 0
        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        scene.setSceneRect(0, 0, 400, 400)
        self.setScene(scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        #==
        self.scale(0.8, 0.8)
        self.setMinimumSize(400, 400)
        self.setWindowTitle("Elastic Nodes")

    #def random_pos_items(self):
        #for item in self.scene().items():
            #if isinstance(item, Node):
                #item.setPos(-150 + QtCore.qrand() % 300, -150 + QtCore.qrand() % 300)

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.delta() / 240.0))

#    def drawBackground(self, painter, rect):
        ## Shadow.
        #sceneRect    = self.sceneRect()
        #rightShadow  = QtCore.QRectF(sceneRect.right(), sceneRect.top() + 5, 5, sceneRect.height())
        #bottomShadow = QtCore.QRectF(sceneRect.left() + 5, sceneRect.bottom(), sceneRect.width(), 5)
        #if rightShadow.intersects(rect) or rightShadow.contains(rect):
			#painter.fillRect(rightShadow, QtCore.Qt.darkGray)
        #if bottomShadow.intersects(rect) or bottomShadow.contains(rect):
			#painter.fillRect(bottomShadow, QtCore.Qt.darkGray)

        ## Fill.
        #gradient = QtGui.QLinearGradient(sceneRect.topLeft(), sceneRect.bottomRight())
        #gradient.setColorAt(0, QtCore.Qt.white)
        #gradient.setColorAt(1, QtCore.Qt.lightGray)
        #painter.fillRect(rect.intersect(sceneRect), QtGui.QBrush(gradient))
        #painter.setBrush(QtCore.Qt.NoBrush)
        #painter.drawRect(sceneRect)

        ## Text.
        #textRect = QtCore.QRectF(sceneRect.left() + 4, sceneRect.top() + 4, sceneRect.width() - 4, sceneRect.height() - 4)
        #message  = "Click and drag the nodes around, and zoom with the mouse wheel or the '+' and '-' keys"

        #font = painter.font()
        #font.setBold(True)
        #font.setPointSize(14)
        #painter.setFont(font)
        #painter.setPen(QtCore.Qt.lightGray)
        #painter.drawText(textRect.translated(2, 2), message)
        #painter.setPen(QtCore.Qt.black)
        #painter.drawText(textRect, message)

    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        print factor
        if factor < 0.07 or factor > 1.6:
            return
        self.scale(scaleFactor, scaleFactor) 

class Graph(object):
    '''
    This class handle every network related
    methods, from analysis  to drawing.
    '''
    def __init__(self, displaywidget):
        self.View       = displaywidget
        self.scene      = self.View.scene()
        #==
  
    def getLayout(self):
        assert False
        #return nx.random_layout(self.G)

    def drawNode(self, real_node, size, pos):
        node = Node(real_node)
        node.setPos(pos[0], pos[1])
        node.size = size
        self.scene.addItem(node)
        return node

    def drawEgde(self, start, end, size):
        ed = Edge(start, end)
        ed.size = size
        self.scene.addItem(ed)
        return ed

#    def centerScene(self, rect):
        #"""
        #centers the scene and fits the specified rectangle to it
        #"""
        #ymax, ymin = rect[3], rect[1]
        #xmax, xmin = rect[2], rect[0]
        #xxs = (xmax-xmin)*1.1 #percentage of extra space
        #yxs = (ymax-ymin)*1.1 #percentage of extra space
        ##calculating center of scene

        #xc = (xmax+xmin)/2.
        #yc = (ymax+ymin)/2.

        ##self.View.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        #self.scene.setSceneRect(xmin, ymin, xxs, yxs)
        #self.View.fitInView(xmin, ymin, xxs, yxs)
        #self.View.setScene(self.scene)
        #self.View.updateSceneRect(self.scene.sceneRect())
        #self.View.centerOn(xc, yc)
        #scale_factor = self.View.width()/xxs
        #self.View.scale(scale_factor, scale_factor)

        #self.View.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        #self.View.setRenderHint(QtGui.QPainter.Antialiasing)
        #self.View.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        #self.View.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
  
#def getRect(nodes):
    #'''
    #Returns the bounding rectangle for the graph
    #'''
    #rect = [0,0,0,0]
    #for n in nodes:
        #rect[0] = n.pos().x() if n.pos().x()<rect[0] else rect[0]
        #rect[1] = n.pos().y() if n.pos().y()<rect[1] else rect[1]
        #rect[2] = n.pos().x() if n.pos().x()>rect[2] else rect[2]
        #rect[3] = n.pos().y() if n.pos().y()>rect[3] else rect[3]
    #return rect
  
class Node(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 1
  
    def __init__(self, real_node):
        self.real_node = real_node
        QtGui.QGraphicsItem.__init__(self)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(1)
        self.edgeList = []
        self.size  = 20

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu()
        menu.addAction("Remove");
        menu.addAction("UnGroup");
        menu.addAction("Pin");
        menu.exec_(event.screenPos())

    def type(self):
        return Node.Type
  
    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(-self.size/2 - adjust, -self.size/2 - adjust,
                              self.size + adjust,  self.size + adjust)

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edgeList:
                edge.adjust()
        return super(Node, self).itemChange(change, value)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(-self.size/2., -self.size/2., self.size,self.size)
        return path
  
    def paint(self, painter, option, widget):
        gradient = QtGui.QRadialGradient(-3, -3, 10)
        gradient.setColorAt(0, QtCore.Qt.yellow)
        gradient.setColorAt(1, QtCore.Qt.darkYellow)
        #==
        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawEllipse(-self.size/2., -self.size/2., self.size,self.size)
  
    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)
  
    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)
  
class Edge(QtGui.QGraphicsItem):
    Type  = QtGui.QGraphicsItem.UserType + 2
  
    def __init__(self, sourceNode, destNode):
        QtGui.QGraphicsItem.__init__(self)
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        #==
        assert sourceNode != destNode
        self.source      = sourceNode
        self.dest        = destNode
        self.adjust()
  
    def type(self):
        return Edge.Type
  
    def setSourceNode(self, node):
        self.source = node
        self.adjust()
  
    def setDestNode(self, node):
        self.dest = node
        self.adjust()
  
    def adjust(self):
        line       = QtCore.QLineF(self.mapFromItem(self.source, 0, 0), self.mapFromItem(self.dest, 0, 0))
        length     = line.length()
        fac        = self.source.size/2.5
        edgeOffset = QtCore.QPointF((line.dx() * fac) / length, (line.dy() * fac) / length)
        self.prepareGeometryChange()
        self.sourcePoint = line.p1() + edgeOffset
        self.destPoint   = line.p2() - edgeOffset
  
    def boundingRect(self):
        #if not self.source or not self.dest:
            #return QtCore.QRectF()
        penWidth = 1
        extra    = penWidth / 2.0
        return QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)
  
    def paint(self, painter, option, widget):
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)
        if line.length() == 0.0:
            return
        #==
        painter.setPen(QtGui.QPen(QtCore.Qt.black, .5, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)
  
if __name__ == "__main__":
    import sys
    app   = QtGui.QApplication(sys.argv)
    MainW = QtGui.QMainWindow()
    sys.exit(app.exec_())
