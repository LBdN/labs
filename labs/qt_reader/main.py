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

P3D_WIN_WIDTH  = 800
P3D_WIN_HEIGHT = 500

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

        self.pandaContainer = QTPandaWidget(self)
        self.pandaContainer.setGeometry(0,0,P3D_WIN_WIDTH,P3D_WIN_HEIGHT)
        #self.pandaContainer.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.layout      = QHBoxLayout()
        self.prop_layout = QVBoxLayout()
        self.prop_layout.insertStretch(-1)
        self.layout.addLayout(self.prop_layout)
        self._3d_layout  = QVBoxLayout()
        self.layout.addLayout(self._3d_layout)
        self._3d_layout.addWidget(self.pandaContainer)
        self.view = qtgraph.GraphWidget()
        self._3d_layout.addWidget(self.view)
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        #==

        # this basically creates an idle task
        timer =  QTimer(self)
        self.connect( timer, SIGNAL("timeout()"), pandaCallback )
        timer.start(0)


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
    ctx_panda = ContextPanda(loader, render)
    ctx_qt    = form
    readers   = reader.reader_prepare(ctx_panda, ctx_qt)
    to_read   = p_base.default_obj(taskMgr, base.camera, Task)
    ctx       = {}
    ctx['layout'] = ctx_qt.prop_layout
    meta_reader = reader.MetaReader(readers)
    meta_reader.read_all([(to_read, ctx)])

    form.centralWidget().setLayout(form.layout)
    form.prop_layout.insertStretch(-1)
    app.exec_()
