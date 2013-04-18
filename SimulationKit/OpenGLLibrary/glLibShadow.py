from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.shadow import *
from OpenGL.GL.ARB.depth_texture import *
from OpenGL.GL.ARB.transpose_matrix import *
from glLibLocals import *
from glLibTexturing import glLibTexture


def glLibShadowResizeShadowMap(newresolution, antialiaslevel=0):
    texturing = glGetBooleanv(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_2D)
    ShadowMapSize = newresolution
    mods = ["depthtex", "clamp"]
    if antialiaslevel == 0:
        pass
    elif antialiaslevel == 1:
        mods.append("filter")
    elif antialiaslevel == 2:
        mods.append("mipmap")
    elif antialiaslevel == 3:
        mods.append("mipmap")
        mods.append("filter")
    elif antialiaslevel == 4:
        mods.append("mipmap blend")
    elif antialiaslevel == 5:
        mods.append("mipmap blend")
        mods.append("filter")
    ShadowMapTexture = glLibTexture(None, mods, [ShadowMapSize, ShadowMapSize])
    if not texturing:
        glDisable(GL_TEXTURE_2D)
    return ShadowMapTexture


def glLibShadowInit(shadowmaps=[[256, 0]]):
    global ShadowMaps
    ShadowMaps = []
    for newmap in shadowmaps:
        ShadowMap = glLibShadowResizeShadowMap(newmap[0], newmap[1])
        ShadowMaps.append([ShadowMap, newmap[0], None])


def glLibCreateShadowBefore(shadowmap, lightpos, lightfocus=(0, 0, 0), lightviewangle=100, near=0.1, far=100.0, offset=0.5):
    ShadowMap = ShadowMaps[shadowmap - GLLIB_SHADOW_MAP1]
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(lightviewangle, 1.0, near, far)
    LightProjectionMatrix = glGetFloatv(GL_PROJECTION_MATRIX)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(lightpos[0], lightpos[1], lightpos[2],
              lightfocus[0], lightfocus[1], lightfocus[2],
              0.0, 1.0, 0.0)
    LightViewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    # Use viewport the same size as the shadow map
    
    glViewport(0, 0, ShadowMap[1], ShadowMap[1])
    glPolygonOffset(offset, offset)
    glEnable(GL_POLYGON_OFFSET_FILL) 
    # eval projection matrix
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadMatrixf([[0.5, 0.0, 0.0, 0.0],
                   [0.0, 0.5, 0.0, 0.0],
                   [0.0, 0.0, 0.5, 0.0],
                   [0.5, 0.5, 0.5, 1.0]])
    glMultMatrixf(LightProjectionMatrix)
    glMultMatrixf(LightViewMatrix)
    TextureMatrix = glGetFloatv(GL_TRANSPOSE_MODELVIEW_MATRIX)
    ShadowMap[2] = TextureMatrix
    glPopMatrix()


def glLibCreateShadowAfter(shadowmap):
    ShadowMap = ShadowMaps[shadowmap - GLLIB_SHADOW_MAP1]
    # Write texture into texture obj
    texturing = glGetBooleanv(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ShadowMap[0])
    glCopyTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, 0, 0, ShadowMap[1], ShadowMap[1])
    glDisable(GL_POLYGON_OFFSET_FILL)
    if not texturing:
        glDisable(GL_TEXTURE_2D)


def glLibEnableShadowShading():
    glBlendFunc(GL_SRC_COLOR, GL_DST_COLOR)
    glEnable(GL_BLEND)


def glLibDisableShadowShading():
    glDisable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def glLibRenderShadowCompareBefore(shadowmap):
    global Texturing
    Texturing = glGetBooleanv(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glEnable(GL_TEXTURE_GEN_R)
    glEnable(GL_TEXTURE_GEN_Q)
    ShadowMap = ShadowMaps[shadowmap - GLLIB_SHADOW_MAP1]
    TextureMatrix = ShadowMap[2]
    # Evaluate where to draw shadows using ARB extension        
    glBindTexture(GL_TEXTURE_2D, ShadowMap[0])
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
    glTexGenfv(GL_S, GL_EYE_PLANE, TextureMatrix[0])
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
    glTexGenfv(GL_T, GL_EYE_PLANE, TextureMatrix[1])
    glTexGeni(GL_R, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
    glTexGenfv(GL_R, GL_EYE_PLANE, TextureMatrix[2])
    glTexGeni(GL_Q, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
    glTexGenfv(GL_Q, GL_EYE_PLANE, TextureMatrix[3])
    # Enable shadow comparison
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE_ARB, GL_COMPARE_R_TO_TEXTURE_ARB)
    # Shadow comparison should be True (in shadow) if r > texture
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_FUNC_ARB, GL_GREATER)
    # Shadow comparison should generate an INTENSITY result
    glTexParameteri(GL_TEXTURE_2D, GL_DEPTH_TEXTURE_MODE_ARB, GL_INTENSITY)
    # Set alpha test to discard false comparisons
    glAlphaFunc(GL_EQUAL, 1.0)


def glLibRenderShadowCompareAfter():
    # reset gl params after comparison
##    if not Texturing: glDisable(GL_TEXTURE_2D)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glDisable(GL_TEXTURE_GEN_R)
    glDisable(GL_TEXTURE_GEN_Q)
