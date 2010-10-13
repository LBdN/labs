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
  
class Graph(object):
    '''
    This class handle every network related
    methods, from analysis  to drawing.
    '''
    def __init__(self, displaywidget):
        self.View       = QtGui.QGraphicsView()
        self.View.scene = QtGui.QGraphicsScene(self.View)
  
    def getLayout(self):
        assert False
        #return nx.random_layout(self.G)

    def drawNode(self, real_node, size, pos):
        node = Node(real_node)
        node.setPos(pos[0], pos[1])
        node.size = size
        self.View.scene.addItem(node)
        return node

    def drawEgde(self, start, end, size):
        ed = Edge(start, end)
        ed.size = size
        self.View.scene.addItem(ed)
        return ed

def centerScene(View, rect):
    """
    centers the scene and fits the specified rectangle to it
    """
    ymax, ymin = rect[3], rect[1]
    xmax, xmin = rect[2], rect[0]
    xxs = (xmax-xmin)*1.1 #percentage of extra space
    yxs = (ymax-ymin)*1.1 #percentage of extra space
    #calculating center of scene

    xc = (xmax+xmin)/2.
    yc = (ymax+ymin)/2.

    View.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
    View.scene.setSceneRect(xmin, ymin, xxs, yxs)
    View.fitInView(xmin, ymin, xxs, yxs)
    View.setScene(View.scene)
    View.updateSceneRect(View.scene.sceneRect())
    View.centerOn(xc, yc)
    scale_factor = View.width()/xxs
    View.scale(scale_factor, scale_factor)

    View.setCacheMode(QtGui.QGraphicsView.CacheBackground)
    View.setRenderHint(QtGui.QPainter.Antialiasing)
    View.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
    View.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
  
def getRect(nodes):
    '''
    Returns the bounding rectangle for the graph
    '''
    rect = [0,0,0,0]
    for n in nodes:
        rect[0] = n.pos.x() if n.pos.x()<rect[0] else rect[0]
        rect[1] = n.pos.y() if n.pos.y()<rect[1] else rect[1]
        rect[2] = n.pos.x() if n.pos.x()>rect[2] else rect[2]
        rect[3] = n.pos.y() if n.pos.y()>rect[3] else rect[3]
    return rect
  
class Node(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 1
  
    def __init__(self, real_node):
        self.real_node = real_node
        QtGui.QGraphicsItem.__init__(self)
        self.newPos = QtCore.QPointF()
#        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setZValue(1)
        self.size  = 20
  
    def type(self):
        return Node.Type
  
    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(-10 - adjust, -10 - adjust,
                              23 + adjust,  23 + adjust)
  
    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(-self.size/2., -self.size/2., self.size,self.size)
        return path
  
    def paint(self, painter, option, widget):
        gradient = QtGui.QRadialGradient(-3, -3, 10)
        if option.state & QtGui.QStyle.State_Sunken:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.yellow).light(120))
            gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkYellow).light(120))
        else:
            gradient.setColorAt(0, QtCore.Qt.yellow)
            gradient.setColorAt(1, QtCore.Qt.darkYellow)
  
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
        painter.setPen(QtGui.QPen(QtCore.Qt.black, .1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)
  
if __name__ == "__main__":
    import sys
    app   = QtGui.QApplication(sys.argv)
    MainW = QtGui.QMainWindow()
    sys.exit(app.exec_())
