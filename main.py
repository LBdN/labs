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
# main program
#----------------------------------------------------------------------

class World(DirectObject):
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

if __name__ == '__main__':
   world = World()
   app   = QApplication(sys.argv)
   form  = QTTest(world.step)
   world.bindToWindow(int(form.winId()))
   form.show()
   app.exec_()
