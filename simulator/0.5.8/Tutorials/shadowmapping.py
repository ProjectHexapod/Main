#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#f             - Toggle shadowmap filtering
#LCLICK + DRAG - Rotate camera
#RCLICK + DRAG - Rotate spaceship
#SROLL WHEEL   - Zoom

#Theory:
#If you were a light source, everything you could see in any
#direction would be lit (i.e., not in shadow).  Shadowmapping
#draws the scene from the light's point of view, recording
#each fragment's depth.  Then, from the camera's perspective,
#for every fragment, if that fragment is further away from the
#light than the fragment it recorded in its depth map, the
#point is in shadow.  Otherwise, it is lit.  

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View3D, LightView, filtering
    global Spaceship, Plane
    global SpaceshipRotation, SpaceshipPosition, CameraRotation, CameraRadius
    global Light1
    global ShadowDrawingShader
    global DiffuseTexture, FloorTexture
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,20)
    #The light's viewpoint.  Try to keep the
    #angle as small as possible to efficiently
    #use the texture's space.  
    LightView = glLibView3D((0,0,512,512),20,5,15)

    Spaceship = glLibObject("data/objects/Spaceship.obj",GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    Spaceship.build_vbo()

    FloorTexture = glLibTexture2D("data/floor.jpg",[0,0,512,512],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    Plane = glLibPlane(5,(0,1,0),FloorTexture,10)

    DiffuseTexture = glLibTexture2D("data/plates.jpg",[0,0,512,512],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    SpaceshipRotation = [0,0]
    SpaceshipPosition = [0,1,0]
    CameraRotation = [90,23]
    CameraRadius = 5.0
    filtering = False

    glEnable(GL_LIGHTING)
    Light1 = glLibLight(1)
    Light1.set_pos([0,10,1])
    #Make this light a point light type
    Light1.set_type(GLLIB_POINT_LIGHT)
    #Set the spot light's direction to straight down.
    Light1.set_spot_dir([0.0,-1.0,0.0])
    #Set the light's angle.  The light's cone
    #will have an apex angle of 15 degrees.
    Light1.set_spot_angle(15.0)
    #Set the light's exponent (the rate at which the intensity drops off
    #as distance increases from the center of the light's cone).  0.0 is
    #the default (no attenuation), but you can play with it.  
    Light1.set_spot_ex(0.0)
    Light1.enable()

    pygame.mouse.get_rel()

    #Add the shadowing calls.  We do .pass_shadow_texture(...,2)
    #below, so we must use shadtex2 here.  "tex2D_1" contains the
    #diffuse texture.  The "clamp" moves shadowed values (0.0) to
    #0.5, making the shadows not completely black; just darker.
    #The second "shadowed_value" creates soft shadows.  These are
    #slower, but nicer.  Note that for somewhat sloped polygons,
    #it creates completely wrong results, such as on the spaceship.
    #light_spot(...) checks to see if the fragment is in the
    #light's spot--in this case, 1.0 if yes, 0.0 if no.

    #If the shadows do not look correct, try commenting out lines
    #163 and 164 and deleting "*light_spot(light1)" in line 73.
    #If they still look wrong, change "false" in line 71 to "true".
    ShadowDrawingShader = glLibShader()
    ShadowDrawingShader.render_equation("""
    color.rgb += ambient_color.rgb*light_ambient(light1).rgb;
    color.rgb += diffuse_color.rgb*light_diffuse(light1).rgb;
    
    float shadowed_value = shadowed(tex2D_2,false)*light_spot(light1);
    color.rgb += shadowed_value*specular_color.rgb*light_specular_ph(light1).rgb;
    
    color.rgb *= texture2D(tex2D_1,uv).rgb;
    color.rgb *= clamp(shadowed_value,0.2,1.0);""")
    errors = ShadowDrawingShader.compile()
##    if errors != "": pygame.quit();raw_input(errors);sys.exit()
##    print "No errors to report with shadowmapping shader (shadowmapping.py)!"
    print errors
    
def quit():
    global Light1, Spaceship
    glDisable(GL_LIGHTING)
    del Light1
    del Spaceship

def GetInput():
    global CameraRadius, filtering
    mrel = pygame.mouse.get_rel()
    mpress = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT: quit(); pygame.quit(); sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: return False
            elif event.key == K_f: filtering = not filtering
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 5: CameraRadius += .2
            if event.button == 4: CameraRadius -= .2
    if mpress[0]:
        CameraRotation[0] += mrel[0]
        CameraRotation[1] += mrel[1]
    if mpress[2]:
        SpaceshipRotation[0] += mrel[0]
        SpaceshipRotation[1] += mrel[1]

#depthmap here is None.  Note that the first
#time glLibMakeShadowMap(...) is called, it is
#still None, but after the first frame, it is
#updated, not recreated, saving time.  
depthmap=None
def TransformOccluders():
    glTranslatef(*SpaceshipPosition)
    glRotatef(SpaceshipRotation[0],0,1,0)
    glRotatef(SpaceshipRotation[1],1,0,0)
def DrawOccluders():
    TransformOccluders()
    Spaceship.draw_vbo()
def SetCamera():
    gluLookAt(camerapos[0],camerapos[1],camerapos[2],\
              SpaceshipPosition[0],SpaceshipPosition[1],SpaceshipPosition[2],\
              0,1,0)
def Draw(Window):
    global camerapos
    #====FIRST PASS====
    
    #Global.  This setup prevents depthmap from
    #being made repeatedly--just updated.  This
    #is vastly more efficent.  
    global depthmap
    #Clear the screen
    Window.clear()
    #Render the light's view of the occluders to a texture.
    depthmap,proj,view = glLibMakeShadowMap(Light1,LightView,SpaceshipPosition,depthmap,DrawOccluders,offset=1.0,filtering=False)
    if filtering: depthmap.filtering(GLLIB_FILTER,False)
    else: depthmap.filtering(False,False)
    
    #====SECOND PASS====
    
    #The screen must now be cleared again
    Window.clear()
    View3D.set_view()
    camerapos = [SpaceshipPosition[0] + CameraRadius*cos(radians(CameraRotation[0]))*cos((radians(CameraRotation[1]))),
                 SpaceshipPosition[1] + CameraRadius*sin(radians(CameraRotation[1])),
                 SpaceshipPosition[2] + CameraRadius*sin(radians(CameraRotation[0]))*cos((radians(CameraRotation[1])))]
    SetCamera()
    
    Light1.set()
    #Draw a sphere at the light's location
    Light1.draw_as_sphere()

    glLibUseShader(ShadowDrawingShader)
    ShadowDrawingShader.pass_texture(DiffuseTexture,1)
    glPushMatrix()
    #Send the shadow textures to "Shader" starting
    #with shadtex2.  "TransformOccluders" rotates the
    #shadow matrix so that the spaceship can be rotated
    #and the shadows still be correct.
    glLibDrawWithShadowMaps([[depthmap,proj,view]],2,ShadowDrawingShader,TransformOccluders)
    #Send the transform and inverse view matrices to
    #the shader.  These are necessary for spot lighting.
    #If spot lighting is not used, this is not necessary.
    glLibSendTransform(ShadowDrawingShader,TransformOccluders)
    glLibSendInvView(ShadowDrawingShader,SetCamera)
    DrawOccluders()
    glPopMatrix()
    
    ShadowDrawingShader.pass_texture(FloorTexture,1)
    #Update the transform matrix (the floor doesn't move).
    glLibSendTransform(ShadowDrawingShader,lambda:0)
    #Send the shadow textures to "Shader" starting
    #with shadtex2.  Because the floor does not get
    #transformed, lambda:0 (null function) is passed.
    glLibDrawWithShadowMaps([[depthmap,proj,view]],2,ShadowDrawingShader,lambda:0)
    Plane.draw()

    glLibUseShader(None)

    Window.flip()
