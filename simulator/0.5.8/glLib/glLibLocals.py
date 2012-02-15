#Mute Warnings (change in production environments)
mute_warnings = False

#Import Errors
import glLibError
import logging

#Import OpenGL
try:
    import OpenGL
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
    from OpenGL import error
    try:glutInit()
    except:
        if not mute_warnings: print "Warning: OpenGL.GLUT initialization failed"
except:
    raise glLibError.glLibError("Error: PyOpenGL not available")

#Import PyGame
try:
    import pygame
    from pygame.locals import *
    pygame.init()
except:
    raise glLibError.glLibError("Error: PyGame not available")

#Import NumPy
try:
    import numpy as np
    try:pygame.surfarray.use_arraytype("numpy")
    except:print "Surfarray not available"
except:
    raise glLibError.glLibError("Error: NumPy not available")

#Import Shaders
GLLIB_SHADERS_AVAILABLE = False
try:
    from OpenGL.GL.ARB.shader_objects import *
    from OpenGL.GL.ARB.vertex_shader import *
    from OpenGL.GL.ARB.fragment_shader import *
    GLLIB_SHADERS_AVAILABLE = True
##    try:
##        from OpenGL.GL.ARB.geometry_shader4 import *
##    except:
##        print "No geometry shaders"
except:
    if not mute_warnings: print "Warning: Shaders not available"

###Import Shadowmapping Extension
##GLLIB_SHADOWMAPS_AVAILABLE = False
##try:
##    from OpenGL.GL.ARB.transpose_matrix import *
##    GLLIB_SHADOWMAPS_AVAILABLE = True
##except:
##    print "Shadowmapping not available"
    
#Import FBO Extension
GLLIB_FRAMEBUFFERS_AVAILABLE = False
try:
    from OpenGL.GL.EXT.framebuffer_object import *
    GLLIB_FRAMEBUFFERS_AVAILABLE = True
except:
    if not mute_warnings: print "Warning: FBOs not available"

#Import 32 Bit Float (High Precision) Textures
GLLIB_FLOAT_TEXTURES_AVAILABLE = False
try:
    from OpenGL.GL.ARB.texture_float import *
    GLLIB_FLOAT_TEXTURES_AVAILABLE = True
except:
    if not mute_warnings: print "Warning: High-precision textures not available"

###Import Texture Compression for 64 Bit (High Precision) Textures
##from OpenGL.GL.EXT.texture_compression_s3tc import *

#Import VBOs
GLLIB_VBO_AVAILABLE = False
try:
    from OpenGL.arrays import vbo
    GLLIB_VBO_AVAILABLE = True
except:
    if not mute_warnings: print "Warning: VBOs not available"

#Import Anisotropy
GLLIB_ANISOTROPY_AVAILABLE = False
try:
    from OpenGL.GL.EXT.texture_filter_anisotropic import *
    GLLIB_ANISOTROPY_AVAILABLE = True
except:
    if not mute_warnings: print "Warning: Anisotropic filtering not available"
    
#Import Other
import sys,os,traceback
from math import *
    
#Locals
#   Misc (1-100)
GLLIB_3D = 1
GLLIB_2D = 2
GLLIB_FALSE = False
GLLIB_TRUE = True
GLLIB_NONE = None
GLLIB_FBCOPY = 3
GLLIB_USING_SHADER = False
GLLIB_MAX = 4
GLLIB_AUTO = 5
GLLIB_CENTER = 6
GLLIB_ALL = 7
#   Filters (101-200)
GLLIB_GAUSS = 101
GLLIB_BLOOM = 102
GLLIB_BOX = [[1,1,1],
             [1,1,1],
             [1,1,1]]
GLLIB_LAPLACIAN = [[ 0,-1, 0],
                   [-1, 4,-1],
                   [ 0,-1, 0]]
GLLIB_SHARPEN = [[ 0,-1, 0],
                 [-1, 5,-1],
                 [ 0,-1, 0]]
GLLIB_DOUBLE_LINE_SHARPEN = [[ 0,-1,-1,-1, 0],
                             [-1, 2,-4, 2,-1],
                             [-1,-4,13,-4,-1],
                             [-1, 2,-4, 2,-1],
                             [ 0,-1,-1,-1, 0]]
#   Draw Type (201-300)
GLLIB_FILL = 201
GLLIB_LINE = 202
GLLIB_OUTLINE = 203
GLLIB_POINT = 204
#   Lighting (301-400)
GLLIB_VERTEX_NORMALS = 301
GLLIB_FACE_NORMALS = 302
GLLIB_POINT_LIGHT = 303
GLLIB_DIRECTIONAL_LIGHT = 304
##GLLIB_SINGLE_SIDE = 305
##GLLIB_DOUBLE_SIDE = 306
#   Texturing (401-500)
GLLIB_MIPMAP = 401
GLLIB_MIPMAP_BLEND = 402
GLLIB_FILTER = 403
GLLIB_CLAMP = 404
GLLIB_REPEAT = 405
GLLIB_MIRROR_REPEAT = 406
GLLIB_TEXTURE_1D = GL_TEXTURE_1D
GLLIB_TEXTURE_2D = GL_TEXTURE_2D
GLLIB_TEXTURE_3D = GL_TEXTURE_3D
GLLIB_TEXTURE_CUBE = GL_TEXTURE_CUBE_MAP
GLLIB_TEXTURE_CUBE_FACES = [GL_TEXTURE_CUBE_MAP_POSITIVE_X,
                            GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
                            GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
                            GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
                            GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
                            GL_TEXTURE_CUBE_MAP_NEGATIVE_Z]
#       Formats
GLLIB_RGB = GL_RGB
GLLIB_RGBA = GL_RGBA
GLLIB_DEPTH = GL_DEPTH_COMPONENT
#   Colors (501-600)
GLLIB_RED = 502
GLLIB_ORANGE = 503
GLLIB_YELLOW = 504
GLLIB_GREEN = 505
GLLIB_BLUE = 506
GLLIB_PURPLE = 507
GLLIB_WHITE = 508
GLLIB_BLACK = 509
GLLIB_GREY = GLLIB_GRAY = 510
GLLIB_PINK = 511
GLLIB_CYAN = 512
#   Materials
GLLIB_MATERIAL_FULL = "mfull"
GLLIB_MATERIAL_BRASS = "mbrass"
GLLIB_MATERIAL_BRONZE = "mbronze"
GLLIB_MATERIAL_CHROME = "mchrome"
GLLIB_MATERIAL_COPPER = "mcopper"
GLLIB_MATERIAL_DEFAULT = "mdefault"
GLLIB_MATERIAL_GOLD = "mgold"
GLLIB_MATERIAL_SILVER = "msilver"
GLLIB_MATERIAL_BLACK_PLASTIC = "mblp"
GLLIB_MATERIAL_CYAN_PLASTIC = "mcp"
GLLIB_MATERIAL_GREEN_PLASTIC = "mgp"
GLLIB_MATERIAL_RED_PLASTIC = "mrp"
GLLIB_MATERIAL_WHITE_PLASTIC = "mwp"
GLLIB_MATERIAL_YELLOW_PLASTIC = "myp"
GLLIB_MATERIAL_BLACK_RUBBER = "mblr"
GLLIB_MATERIAL_CYAN_RUBBER = "mcr"
GLLIB_MATERIAL_GREEN_RUBBER = "mgr"
GLLIB_MATERIAL_RED_RUBBER = "mrr"
GLLIB_MATERIAL_WHITE_RUBBER = "mwr"
GLLIB_MATERIAL_YELLOW_RUBBER = "myr"
#   Shaders (601-700)
GLLIB_PHONG = 601
GLLIB_BLINN = 602
GLLIB_TEXTURE = 603
GLLIB_VIEW_DEPTHBUFFER = 604
GLLIB_VIEW_NORMALS = 605
GLLIB_BLANK = 606
GLLIB_DEPTH_PEEL = 607
GLLIB_DEPTH_PEEL_SINGLE_PASS = 608
GLLIB_POSITION_MAP = 609
GLLIB_CAUSTIC_MAP = 610
GLLIB_PARTICLE_DRAW = 611
GLLIB_PARTICLE_UPDATE = 612
GLLIB_CLOTH_DISTANCE = 613
GLLIB_CLOTH_UPDATE = 614
GLLIB_CLOTH_COLLIDE = 615
GLLIB_CLOTH_NORMAL = 616
GLLIB_CLOTH_DRAW = 617
GLLIB_HAIR_GROW = 618
GLLIB_HAIR_UPDATE = 619
GLLIB_HAIR_DRAW = 620
GLLIB_FLUID2D_DIFFUSE = 621
GLLIB_FLUID2D_ADVECT = 622
#   Obstacles (701-800)
GLLIB_OBSTACLE_SPHERE = 701
GLLIB_OBSTACLE_BOX = 702
#   Characters (801-900)
GLLIB_MALE = 801
GLLIB_FEMALE = 802
GLLIB_CHARACTER_LEFTHIP = 803
GLLIB_CHARACTER_RIGHTHIP = 804
GLLIB_CHARACTER_LEFTKNEE = 805
GLLIB_CHARACTER_RIGHTKNEE = 806
GLLIB_CHARACTER_LEFTANKLE = 807
GLLIB_CHARACTER_RIGHTANKLE = 808
GLLIB_CHARACTER_PELVIS = 809
GLLIB_CHARACTER_BACK = 810
GLLIB_CHARACTER_LEFTSHOULDER = 811
GLLIB_CHARACTER_RIGHTSHOULDER = 812
GLLIB_CHARACTER_LEFTELBOW = 813
GLLIB_CHARACTER_RIGHTELBOW = 814
#   Clothes (901-1000)
GLLIB_CLOTHES_SHORTS = 901
GLLIB_CLOTHES_LONGPANTS = 902
GLLIB_CLOTHES_SKIRT = 903
GLLIB_CLOTHES_DRESS = 904
GLLIB_CLOTHES_SHIRT = 905
GLLIB_CLOTHES_STRAPLESSTOP = 906
GLLIB_CLOTHES_BUTTONSHIRT = 907
GLLIB_CLOTHES_COAT = 908
GLLIB_CLOTHES_SUITJACKET = 909
GLLIB_CLOTHES_TRENCHCOAT = 910
GLLIB_CLOTHES_CAPE = 911
GLLIB_CLOTHES_CLOAK = 912
GLLIB_CLOTHES_NECKTIE = 913
GLLIB_CLOTHES_BOWTIE = 914
GLLIB_CLOTHES_SCARF = 915
