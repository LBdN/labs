from pandac.PandaModules import Vec3


P3D_VERSION = '0.1'


__version__ = P3D_VERSION


X_AXIS = Vec3(1, 0, 0)
Y_AXIS = Vec3(0, 1, 0)
Z_AXIS = Vec3(0, 0, 1)


import commonUtils
from object      import Object
from marquee     import Marquee
from camera      import *
from mouse       import *
from mousePicker import *
import geometry
