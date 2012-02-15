from glLibLocals import *
from glLibTexturing import *
class glLibFBO:
    def __init__(self,size,depthsize=8):
        self.size = list(size)
        
        self.textures = {}
        self.render_buffers = {}
        
        self.framebuffer = glGenFramebuffersEXT(1)
        self.renderbuffer = glGenRenderbuffersEXT(1)
        
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,self.framebuffer)
        glBindRenderbufferEXT(GL_RENDERBUFFER_EXT,self.renderbuffer)
        
        if   depthsize ==  8: glRenderbufferStorageEXT(GL_RENDERBUFFER_EXT,GL_DEPTH_COMPONENT,  size[0],size[1])
        elif depthsize == 16: glRenderbufferStorageEXT(GL_RENDERBUFFER_EXT,GL_DEPTH_COMPONENT16,size[0],size[1])
        elif depthsize == 24: glRenderbufferStorageEXT(GL_RENDERBUFFER_EXT,GL_DEPTH_COMPONENT24,size[0],size[1])
        elif depthsize == 32: glRenderbufferStorageEXT(GL_RENDERBUFFER_EXT,GL_DEPTH_COMPONENT32,size[0],size[1])
        
        glFramebufferRenderbufferEXT(GL_FRAMEBUFFER_EXT,GL_DEPTH_ATTACHMENT_EXT,GL_RENDERBUFFER_EXT,self.renderbuffer)
        
        glBindRenderbufferEXT(GL_RENDERBUFFER_EXT,0)
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,0)
        
        self.status = self.check_status()
    def add_render_target(self,number,type=GLLIB_RGB,filter=False,mipmap=False,precision=8):
        newtexture = glLibTexture2D(None,[0,0,self.size[0],self.size[1]],type,filter,mipmap,None,precision)
        if type == GLLIB_DEPTH: attachment = GL_DEPTH_ATTACHMENT_EXT
        else:                   attachment = GL_COLOR_ATTACHMENT0_EXT+number
        self.textures[number] = newtexture
        if attachment == GL_DEPTH_ATTACHMENT_EXT: self.render_buffers[number] = GL_NONE
        else:                                     self.render_buffers[number] = attachment
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,self.framebuffer)
        glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT,attachment,GL_TEXTURE_2D,self.textures[number].texture,0)
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,0)
    def set_render_target(self,number,newtexture):
        try:
            del self.textures[number]
            del self.render_buffers[number]
        except:pass
        self.textures[number] = newtexture
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,self.framebuffer)
        glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT,GL_COLOR_ATTACHMENT0_EXT+number,GL_TEXTURE_2D,self.textures[number].texture,0)
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,0)
    def remove_render_target(self,number):
        del self.textures[number]
        del self.render_buffers[number]
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,self.framebuffer)
        glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT,GL_COLOR_ATTACHMENT0_EXT+number,GL_TEXTURE_2D,0,0)
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,0)
    def check_status(self):
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,self.framebuffer)
        self.enable(GLLIB_ALL)
        status = glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT)
        self.disable()
        if   status == GL_FRAMEBUFFER_COMPLETE_EXT:
            status =  "GL_FRAMEBUFFER_COMPLETE_EXT"
        elif status == GL_FRAMEBUFFER_UNSUPPORTED_EXT:
            status =  "GL_FRAMEBUFFER_UNSUPPORTED_EXT"
        elif status == GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT_EXT:
            status =  "GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT_EXT"
        elif status == GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT_EXT:
            status =  "GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT_EXT"
        elif status == GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS_EXT:
            status =  "GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS_EXT"
        elif status == GL_FRAMEBUFFER_INCOMPLETE_FORMATS_EXT:
            status =  "GL_FRAMEBUFFER_INCOMPLETE_FORMATS_EXT"
        elif status == GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER_EXT:
            status =  "GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER_EXT"
        elif status == GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER_EXT:
            status =  "GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER_EXT"
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,0)
        self.status = status
        return status #GL_FRAMEBUFFER_COMPLETE_EXT
    def enable(self,list):
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,self.framebuffer)
        if list == GLLIB_ALL: list = self.textures.keys()
        array = []
        for key in list:
            array.append(self.render_buffers[key])
        glDrawBuffers(len(list),np.array(array))
    def disable(self):
        glDrawBuffers(1,np.array([GL_COLOR_ATTACHMENT0_EXT]))
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,0)
    def get_texture(self,rendertarget):
        return self.textures[rendertarget]
