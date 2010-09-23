# -*- coding: UTF-8 -*-


from PyQt4.QtCore        import *
from PyQt4.QtGui         import *

P3D_WIN_WIDTH  = 800
P3D_WIN_HEIGHT = 500

from direct.showbase.DirectObject import *
from pandac.PandaModules          import WindowProperties
from pandac.PandaModules          import loadPrcFileData
from pandac.PandaModules          import *

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

        #hellobutton = Qt.QPushButton("Say 'Hello world!'",None)
        ## And connect the action "sayHello" to the event "button has been clicked"
        #self.connect(hellobutton, Qt.SIGNAL("clicked()"), sayHello)

        #self.lineedit = QLineEdit("Proba ugnjezdenog prikaza...")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.pandaContainer)
        #layout.addWidget(self.lineedit)
        #layout.addWidget(self.lineedit)
        #layout.addWidget(self.lineedit)
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

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


if __name__ == '__main__':
    world = PandaPseudoWindow()
    app   = QApplication(sys.argv)
    form  = QTTest(world.step)
    world.bindToWindow(int(form.winId()))
    form.show()
    
    import reader, p_base
    readers = reader.reader_prepare(loader, render, form.layout, form.connect)
    to_read = p_base.default()
    reader.read_all(to_read, readers)

    app.exec_()
