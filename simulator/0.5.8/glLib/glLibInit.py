from glLibLocals import *
def glLibInternal_init():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
    glTexEnvi(GL_POINT_SPRITE,GL_COORD_REPLACE,GL_TRUE)
    glMaterialf(GL_FRONT_AND_BACK,GL_SHININESS,1.0)
    glEnable(GL_DEPTH_TEST)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST)
    glEnable(GL_TEXTURE_2D)
def glLibInternal_init_shaders():
    glInitShaderObjectsARB()
    glInitVertexShaderARB()
    glInitFragmentShaderARB()
    
    
