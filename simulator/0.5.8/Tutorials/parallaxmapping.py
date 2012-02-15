#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#LCLICK + DRAG - Rotate camera
#RCLICK + DRAG - Rotate spaceship
#SROLL WHEEL   - Zoom

#Theory:
#The basic color at a pixel is really just the object's texture's
#value.  By adjusting the texture coordinates according to how
#"deep" they are, the appearance of truly 3D objects can be
#simulated.  This is called "parallax mapping".  If self-occlusion
#of the surface is taken into account, the result is slower but
#often more realistic.  This effect is called "parallax occlusion
#mapping".

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View3D, Light1, Shader
    global Spaceship, Plane
    global SpaceshipRotation
    global CameraRotation, CameraRadius
    global DiffuseTexture, Normalmap, Heightmap
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,20)

    Spaceship = glLibObject("data/objects/Spaceship.obj",GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    Spaceship.build_vbo()

    FloorTexture = glLibTexture2D("data/floor.jpg",[0,0,512,512],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    Plane = glLibPlane(5,(0,1,0),FloorTexture,10)

    DiffuseTexture = glLibTexture2D("data/rock.jpg",[0,0,256,256],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    Normalmap = glLibTexture2D("data/rocknormal.png",[0,0,255,255],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    #Load a heightmap
    Heightmap = glLibTexture2D("data/rockheight.png",[0,0,256,256],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    SpaceshipRotation = [0,0]
    CameraRotation = [90,23]
    CameraRadius = 5.0

    glEnable(GL_LIGHTING)
    Light1 = glLibLight(1)
    Light1.set_pos([0,10,0])
    Light1.enable()

    pygame.mouse.get_rel()

    Shader = glLibShader()
    
    Shader.render_equation("""
    normal = normal_from_normalmap(tex2D_2,uv);
    color.rgb += ambient_color.rgb*light_ambient(light1).rgb;
    color.rgb += diffuse_color.rgb*light_diffuse(light1).rgb;
    color.rgb += specular_color.rgb*light_specular_ph(light1).rgb;
    color.rgb *= texture2D(tex2D_1,uv).rgb;""")
    #These effects are entirely based off of displacing
    #texture coordinates.  Look it up.  These functions
    #do this displacement.  "tex2D_3" is the heightmap.  See
    #below.  "parallaxmap(...)" is faster, but more
    #inaccurate.  "parallax_occlusionmap(...)" is slower
    #but more accurate.
    Shader.uv_transform("""
    uv *= 10.0;
    //vec2 offset = parallaxmap(tex2D_3,uv,0.03,false);
    vec2 offset = parallax_occulsionmap(tex2D_3,uv,2.0,false,40,10);
    //vec2 offset = parallax_occulsionmap2(tex2D_3,vec2(256.0,256.0),uv,0.1,false,10); //beta (i.e., won't work)
    uv += offset;""")
    errors = Shader.compile()
##    Shader.print_fragment()
    print errors
##    if errors != "":
##        pygame.quit()
##        raw_input(errors)
##        sys.exit()
##    else:
##        print "No errors to report with parallaxmapping shader (parallaxmapping.py)!"

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

def Draw(Window):
    Window.clear()
    View3D.set_view()
    camerapos = [0 + CameraRadius*cos(radians(CameraRotation[0]))*cos((radians(CameraRotation[1]))),
                 1 + CameraRadius*sin((radians(CameraRotation[1]))),
                 0 + CameraRadius*sin(radians(CameraRotation[0]))*cos((radians(CameraRotation[1])))]
    gluLookAt(camerapos[0],camerapos[1],camerapos[2], 0,1,0, 0,1,0)
    Light1.set()

    glLibUseShader(Shader)
    Shader.pass_texture(DiffuseTexture,1)
    Shader.pass_texture(Normalmap,2)
    #Pass the heightmap to "tex3".  
    Shader.pass_texture(Heightmap,3)

    glPushMatrix()
    glTranslatef(0.0,1.0,0.0)
    glRotatef(SpaceshipRotation[0],0,1,0)
    glRotatef(SpaceshipRotation[1],1,0,0)
    Spaceship.draw_vbo(Shader)
    glPopMatrix()
    
    glLibUseShader(None)
    Plane.draw()

    Window.flip()
