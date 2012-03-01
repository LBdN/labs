# -*- coding: UTF-8 -*-
#import gtk
#del gtk

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import sys
def debug_trace():
  '''Set a tracepoint in the Python debugger that works with Qt'''
  from PyQt4.QtCore import pyqtRemoveInputHook
  from pdb          import set_trace
  pyqtRemoveInputHook()
  set_trace()
sys.modules["__builtin__"].__dict__['debug_func'] = debug_trace

P3D_WIN_WIDTH  = 640
P3D_WIN_HEIGHT = 400

import qtgraph

from direct.showbase.DirectObject import *
from pandac.PandaModules          import WindowProperties
from pandac.PandaModules          import loadPrcFileData
from pandac.PandaModules          import *
from direct.task                  import Task
from math                         import *

import sys

#loadPrcFileData("", "fullscreen 1")
loadPrcFileData("", "window-title Bridge")
loadPrcFileData("", "window-type none")

import direct.directbase.DirectStart

#----------------------------------------------------------------------
# PyQt GUI (taken from dinoint's 'post)
#----------------------------------------------------------------------


class QTTest(QMainWindow):
    def __init__(self, pandaCallback, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setWindowTitle("Test")
        self.setGeometry(30,30,800,700)
        #==
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self.main_layout  = QVBoxLayout()
        centralWidget.setLayout(self.main_layout)
        #==
        self.pandaContainer = QTPandaWidget(self)
        self.pandaContainer.setGeometry(0,0,P3D_WIN_WIDTH,P3D_WIN_HEIGHT)
        #self.pandaContainer.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.main_layout.addWidget(self.pandaContainer)
        #==
        self.ldock = QDockWidget(self.tr("Nodes Properties"), self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.ldock)
        self.layout = QVBoxLayout()
        self.prop_widget = QWidget(self)
        self.prop_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        #self.prop_widget.setMinimumSize(400, 800)
        self.prop_widget.setLayout(self.layout)
        self.scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.prop_widget)
        self.ldock.setWidget(self.scrollarea)
        self.prop_widget.show()
        #==
        self.bdock = QDockWidget(self.tr("Transformation Graph"), self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.bdock)
        #==
        self.view = qtgraph.GraphWidget()
        self.bdock.setWidget(self.view)
        #==
        # this basically creates an idle task
        self.timer =  QTimer(self)
        self.timer.timeout.connect(pandaCallback)
        #self.connect( timer, SIGNAL("timeout()"), pandaCallback )
        self.timer.start(0)
        #==
        self.timers = []

    def set_timer(self, interval, callback):
        timer =  QTimer(self)
        timer.timeout.connect(callback)
        timer.start(interval)


#----------------------------------------------------------------------
# main program
#----------------------------------------------------------------------


class QTPandaWidget(QWidget):
   def __init__(self, parent=None):
      super(QWidget, self).__init__(parent)
      self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
      
   def resizeEvent(self, evt):
      wp = WindowProperties()
      wp.setSize(self.width(), self.height())
      wp.setOrigin(self.x(),self.y())
      base.win.requestProperties(wp)
   
   def minimumSizeHint(self):
      return QSize(P3D_WIN_WIDTH,P3D_WIN_HEIGHT)


class PandaPseudoWindow(DirectObject):
    def __init__(self):
        base.disableMouse()

    def bindToWindow(self, windowHandle):
        wp = WindowProperties().getDefault()
        wp.setOrigin(0,0)
        wp.setSize(P3D_WIN_WIDTH, P3D_WIN_HEIGHT)
        wp.setParentWindow(windowHandle)
        base.openDefaultWindow(props=wp)

    def step(self):
        taskMgr.step()

class ContextPanda(object):
    def __init__(self, loader, render):
        self.loader = loader
        self.render = render

    def load(self, path):
        obj = self.loader.loadModel(path)
        obj.reparentTo(self.render)
        return obj


def main():
    world = PandaPseudoWindow()
    app   = QApplication(sys.argv)
    form  = QTTest(world.step)
    world.bindToWindow(int(form.winId()))
    form.show()
    
    import reader, p_base
    #==
    ctx_panda   = ContextPanda(loader, render)
    readers     = reader.reader_prepare()
    meta_reader = reader.QTMetaReader(readers, ctx_panda)
    #==
    ctx_qt    = form
    to_read   = p_base.default_obj()
    ctx       = {}
    ctx['layout'] = ctx_qt.layout
    ctx['widget'] = ctx_qt.prop_widget
    meta_reader.read_all([(to_read, ctx)])
    #==
    ctx       = {}
    io_meta_reader = reader.IOMetaReader(reader.io_readers(), "test.io.json")
    io_meta_reader.read_all([(to_read, {})])
    form.set_timer(1000, io_meta_reader.write) 
    ctx_qt.prop_widget.show()
    app.exec_()
