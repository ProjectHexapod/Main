#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#LCLICK + DRAG - Rotate camera
#RCLICK + DRAG - Rotate spaceship
#SROLL WHEEL   - Zoom

#Theory
#The screen is a "framebuffer" of types.  Scenes are rendered to
#the current framebuffer(s).  Normally, that's the screen, but
#by using off-screen renderbuffers, larger scenes can be
#rendered.  The accuracy (and hence usability) of shadowmapping
#depends to a large degree on the size of the depthmap--the
#larger, the more accurate it is.  Normally, the size of the
#shadowmap would be dependent on the size of the screen's
#framebuffer.  By rendering the depthmap in a separate
#framebuffer, a higher resolution, and hence higher accuracy,
#can be achieved.

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View3D, LightView
    global Spaceship, Plane
    global SpaceshipPosition, SpaceshipRotation, CameraRotation, CameraRadius
    global Light1, fbo
    global Shader
    global DiffuseTexture, FloorTexture
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,20)
    shadowmapsize = 1024
    LightView = glLibView3D((0,0,shadowmapsize,shadowmapsize),20,0.1,20)

    Spaceship = glLibObject("data/objects/Spaceship.obj",GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    Spaceship.build_vbo()

    FloorTexture = glLibTexture2D("data/floor.jpg",[0,0,512,512],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    Plane = glLibPlane(5,(0,1,0),FloorTexture,10)

    DiffuseTexture = glLibTexture2D("data/plates.jpg",[0,0,512,512],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    SpaceshipPosition = [0.0,1.0,0.0]
    SpaceshipRotation = [0,0]
    CameraRotation = [90,23]
    CameraRadius = 5.0
##    CameraRotation = [115,13]
##    CameraRadius = 1.2

    #Make a framebuffer.  We want it to be
    #the same size as the light's view.  The
    #view can now be (way) larger than the
    #Screen (800,600)!
    fbo = glLibFBO((shadowmapsize,shadowmapsize))
    fbo.add_render_target(1,type=GLLIB_DEPTH)

    glEnable(GL_LIGHTING)
    Light1 = glLibLight(1)
    Light1.set_pos([0,10,1])
    Light1.enable()

    pygame.mouse.get_rel()

    Shader = glLibShader()
    #If the shadows do not look right, change "false" to "true"
    #in this shader.
    Shader.render_equation("""
    color.rgb += ambient_color.rgb*light_ambient(light1).rgb;
    color.rgb += diffuse_color.rgb*light_diffuse(light1).rgb;
    color.rgb += specular_color.rgb*light_specular_ph(light1).rgb;
    
    float shadowed_value = shadowed(tex2D_2,false);
    color.rgb *= texture2D(tex2D_1,uv).rgb;
    color.rgb *= clamp(shadowed_value,0.5,1.0);""")
    errors = Shader.compile()
    print errors
##    if errors != "": pygame.quit();raw_input(errors);sys.exit()
##    print "No errors to report with shadowmapping shader (framebuffer.py)!"

def quit():
    global Light1, Spaceship
    glDisable(GL_LIGHTING)
    del Light1
    del Spaceship

def GetInput():
    global CameraRadius
    mrel = pygame.mouse.get_rel()
    mpress = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT: quit(); pygame.quit(); sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE: return False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 5: CameraRadius += .2
            if event.button == 4: CameraRadius -= .2
    if mpress[0]:
        CameraRotation[0] += mrel[0]
        CameraRotation[1] += mrel[1]
    if mpress[2]:
        SpaceshipRotation[0] += mrel[0]
        SpaceshipRotation[1] += mrel[1]

def TransformOccluders():
    glTranslatef(*SpaceshipPosition)
    glRotatef(SpaceshipRotation[0],0,1,0)
    glRotatef(SpaceshipRotation[1],1,0,0)
def DrawOccluders():
    TransformOccluders()
    Spaceship.draw_vbo()
def Draw(Window):
    #====FIRST PASS====

    depthmap,proj,view = glLibMakeShadowMapFBO(fbo,Light1,LightView,SpaceshipPosition,DrawOccluders)
    
    #====SECOND PASS====

    Window.clear()
    View3D.set_view()
    camerapos = [0 + CameraRadius*cos(radians(CameraRotation[0]))*cos((radians(CameraRotation[1]))),
                 1 + CameraRadius*sin((radians(CameraRotation[1]))),
                 0 + CameraRadius*sin(radians(CameraRotation[0]))*cos((radians(CameraRotation[1])))]
    gluLookAt(camerapos[0],camerapos[1],camerapos[2], 0,1,0, 0,1,0)
    
    Light1.set()
    Light1.draw_as_sphere()

    glLibUseShader(Shader)
    Shader.pass_texture(DiffuseTexture,1)
    glPushMatrix()
    glLibDrawWithShadowMaps([[depthmap,proj,view]],2,Shader,TransformOccluders)
    DrawOccluders()
    glPopMatrix()
    
    Shader.pass_texture(FloorTexture,1)
    glLibDrawWithShadowMaps([[depthmap,proj,view]],2,Shader,lambda:0)
    Plane.draw()

    glLibUseShader(None)

    Window.flip()
