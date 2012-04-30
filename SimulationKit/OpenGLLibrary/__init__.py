from OpenGL.GL import *
from OpenGL.GLU import *
from glLibMisc import *
from glLibLocals import *
from glLibWindow import *
from glLibShadow import *
from glLibCamera import glLibCamera
from glLibObjects import glLibObjMap, glLibObjUser, glLibObjText, glLibObjFromFile, glLibObjCube, glLibObjTexCube, glLibObjTeapot, glLibObjSphere, glLibObjTexSphere, glLibObjCylinder, glLibObjTexCylinder, glLibObjCapsule, glLibObjCone, glLibObjTexCone
from glLibLighting import *
from glLibTexturing import *

import inspect, os
# This is the directory where the texture images can be found
TEXTURE_DIR = os.path.dirname(inspect.getfile(inspect.currentframe())) + '/Textures/'

