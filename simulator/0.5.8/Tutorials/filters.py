#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#LCLICK + DRAG - Rotate camera
#RCLICK + DRAG - Rotate spaceship
#SROLL WHEEL   - Zoom

#Theory:
#The accumulation buffer, though not supported everywhere,
#allows filtering farily easily.  The scene is rendered to
#a texture, and then that texture is drawn to the screen
#in different places, being acculuated in the accumulation
#buffer.  Filtering can thus be accomplished.

import sys,os,time
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View2D, View3D, LightView
    global Spaceship, Plane
    global SpaceshipRotation, CameraRotation, CameraRadius
    global Light1, UseFBO, fbo, time1
    global Shader
    global DiffuseTexture, FloorTexture
    View2D = glLibView2D((0,0,Screen[0],Screen[1]))
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,20)

    #Set to true to use framebuffer objects
    UseFBO = False

    if UseFBO: LightView = glLibView3D((0,0,1024,1024),20,0.1,20)
    else: LightView = glLibView3D((0,0,512,512),20,0.1,20)

    Spaceship = glLibObject("data/objects/Spaceship.obj",GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    Spaceship.build_vbo()

    FloorTexture = glLibTexture2D("data/floor.jpg",[0,0,512,512],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    Plane = glLibPlane(5,(0,1,0),FloorTexture,10)

    DiffuseTexture = glLibTexture2D("data/plates.jpg",[0,0,512,512],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    SpaceshipRotation = [0,0]
    CameraRotation = [90,23]
    CameraRadius = 5.0

    if UseFBO:
        fbo = glLibFBO((1024,1024))
        fbo.add_render_target(0)

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
##    print "No errors to report with shadowmapping shader (filters.py)!"

    time1 = time.time()
    
def quit():
    global Light1, Spaceship
    glDisable(GL_LIGHTING)
    del Light1
    del Spaceship

on_filter = 1
def GetInput():
    global CameraRadius,time1,on_filter
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
    time2 = time.time()
    if time2-time1 >= 1:
        time1 = time.time()
        on_filter += 1
        if on_filter == 7:
            on_filter = 1

depthmap=None
scenemap=None
def TransformOccluders():
    glTranslatef(0.0,1.0,0.0)
    glRotatef(SpaceshipRotation[0],0,1,0)
    glRotatef(SpaceshipRotation[1],1,0,0)
def DrawOccluders():
    TransformOccluders()
    Spaceship.draw_vbo()
def Draw(Window):
    global depthmap,scenemap
    Window.clear()

    if UseFBO: fbo.enable([0])
    
    depthmap,proj,view = glLibMakeShadowMap(Light1,LightView,[0,1.0,0],depthmap,DrawOccluders,filtering=GLLIB_FILTER)

    if UseFBO: fbo.disable()
    
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

    #Render scene to texture
    scenemap = glLibSceneToTexture(View3D.rect,scenemap,GLLIB_RGB,filtering=GLLIB_FILTER)
    Window.clear()
    if   on_filter == 1: glLibAccumFilter(scenemap,View2D,GLLIB_BOX) #Mean (box) blur
    elif on_filter == 2: glLibAccumFilter(scenemap,View2D,GLLIB_LAPLACIAN) #Laplacian edge finding filter
    elif on_filter == 3: glLibAccumFilter(scenemap,View2D,GLLIB_SHARPEN) #Sharpen Filter
    elif on_filter == 4: glLibAccumFilter(scenemap,View2D,GLLIB_DOUBLE_LINE_SHARPEN) #Sharpens, but flips colors at edge
    elif on_filter == 5: glLibAccumSeparableFilter(scenemap,View2D,GLLIB_GAUSS,[39,39]) #Gaussian blur with huge kernel
    elif on_filter == 6: glLibAccumSeparableFilter(scenemap,View2D,[[0.5,1.0,0.5],[0.5,1.0,0.5]],[3,3]) #Another blurring filter

    Window.flip()
