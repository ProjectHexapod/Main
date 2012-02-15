#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#n             - Toggles using/not using normalmap
#r             - Toggles reflection/refraction
#LCLICK + DRAG - Rotate camera
#RCLICK + DRAG - Rotate spaceship
#SROLL WHEEL   - Zoom

#Theory:
#Reflections and refractions are really neat, but difficult to
#implement in OpenGL.  A common approach is to render the
#surrounding scene ("environment") in every direction, and then
#simply use the reflected ray or refracted ray's direction to
#look up the proper color from the stored map.  Each of 6
#directions is rendered and the result stored in a "cubemap".
#This isn't correct unless the environment is infinitely far
#away, but in practice the result is visually fairly good.  

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View3D, CubemapView
    global Spaceship, Plane, EnvCube, Cubemap
    global SpaceshipRotation, CameraRotation, CameraRadius
    global Light1
    global Shader
    global Normalmap
    global using_normalmap, reflect_refract
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,200)
    #Cubemap view.  Angle must be 90 degrees.
    CubemapView = glLibView3D((0,0,512,512),90)

    Spaceship = glLibObject("data/objects/Spaceship.obj",GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    #give the spaceship a soft shininess, leave the other material parameters alone.  
    Spaceship.set_material([[-1,-1,-1,1.0],0,-1]) 
    Spaceship.build_vbo()

    FloorTexture = glLibTexture2D("data/floor.jpg",[0,0,512,512],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    Plane = glLibPlane(5,(0,1,0),FloorTexture,10)

    Normalmap = glLibTexture2D("data/rocknormal.png",[0,0,255,255],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    #Load environment textures
    texturenames = []
    for texturename in ["xpos","xneg","ypos","yneg","zpos","zneg"]:
        texturenames.append("data/cubemaps/"+texturename+".jpg")
    textures = []
    for texturename in texturenames:
        texture = glLibTexture2D(texturename,(0,0,256,256),GLLIB_RGB,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
        texture.edge(GLLIB_CLAMP)
        textures.append(texture)
    #Make a 3D cube using these textures of size 100.0
    EnvCube = glLibRectangularSolid([100.0,100.0,100.0],textures)

    #Make a cubemap texture.  Pass None in for the texture data.  The
    #texture will be updated dynamically with glLibUpdateCubeMap(...)
    Cubemap = glLibTextureCube([None]*6,(0,0,512,512),GLLIB_RGB,GLLIB_FILTER)

    SpaceshipRotation = [0,0]
    CameraRotation = [90,23]
    CameraRadius = 5.0

    glEnable(GL_LIGHTING)
    Light1 = glLibLight(1)
    Light1.set_pos([0,10,0])
    Light1.enable()

    pygame.mouse.get_rel()

    #"cubenorm" is a normal, derived from the object's normal that can be
    #sampled in cubemap_reflect_sample(...) and/or cubemap_refract_sample(...).
    #cubemap_normal_from_normalmap(...) does the same, but from a normalmap.  
    Shader = glLibShader()
    #Custom variables
    Shader.user_variables("uniform bool using_normalmap;uniform int reflect_refract;")
    Shader.render_equation("""
    vec3 cubenorm=vec3(0.0);
    if (using_normalmap) { cubenorm = cubemap_normal(); }
    else                 { cubenorm = cubemap_normal_from_normalmap(tex2D_2,uv); }
    
    vec4 reflectsample = cubemap_reflect_sample(texCube_1,cubenorm);
    vec4 refractsample = cubemap_refract_sample(texCube_1,cubenorm,0.66);
    
    if      (reflect_refract==1) { color.rgb = reflectsample.rgb; }
    else if (reflect_refract==2) { color.rgb = refractsample.rgb; }""")
    Shader.uv_transform("uv*=10.0;")
    #Because we have a cube map, we'll need to send it to texCube_1 in the shader.
    Shader.max_textures_cube(1)
    errors = Shader.compile()
    print errors
##    if errors != "":
##        pygame.quit()
##        raw_input(errors)
##        sys.exit()
##    else:
##        print "No errors to report with cubemapping shader (cubemapping.py)!"

    #variables for uniforms that determine whether the shader uses
    #a normalmap, and whether it uses reflection, refraction, or both.
    using_normalmap, reflect_refract = False, 1
        
def quit():
    global Light1, Spaceship
    glDisable(GL_LIGHTING)
    del Light1
    del Spaceship

def GetInput():
    global CameraRadius
    global using_normalmap, reflect_refract
    mrel = pygame.mouse.get_rel()
    mpress = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT: quit(); pygame.quit(); sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE: return False
            elif event.key == K_n: using_normalmap = not using_normalmap
            elif event.key == K_r:
                reflect_refract += 1
                if reflect_refract == 3: reflect_refract = 1
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 5: CameraRadius += .2
            if event.button == 4: CameraRadius -= .2
    if mpress[0]:
        CameraRotation[0] += mrel[0]
        CameraRotation[1] += mrel[1]
    if mpress[2]:
        SpaceshipRotation[0] += mrel[0]
        SpaceshipRotation[1] += mrel[1]

def draw_env_cube():
    glDisable(GL_LIGHTING)
    EnvCube.draw()
    glEnable(GL_LIGHTING)
def draw_reflectees():
    Light1.set()
    draw_env_cube()
    Plane.draw()
def spaceship_rotate():
    glRotatef(SpaceshipRotation[0],0,1,0)
    glRotatef(SpaceshipRotation[1],1,0,0)
def Draw(Window):
    #Update the cubemap.  Draws the environment with
    #draw_reflectees() 6 times.
    glLibSelectTexture(Cubemap)
    glLibUpdateCubeMap([0,1,0],CubemapView,draw_reflectees)
    
    Window.clear()
    View3D.set_view()
    camerapos = [0 + CameraRadius*cos(radians(CameraRotation[0]))*cos((radians(CameraRotation[1]))),
                 1 + CameraRadius*sin((radians(CameraRotation[1]))),
                 0 + CameraRadius*sin(radians(CameraRotation[0]))*cos((radians(CameraRotation[1])))]
    gluLookAt(camerapos[0],camerapos[1],camerapos[2], 0,1,0, 0,1,0)
    Light1.set()

    glLibUseShader(Shader)
     
    glPushMatrix()
    glLoadIdentity()
    spaceship_rotate()
    #Pass the cubemap matrix (contains the rotations only
    #of the reflective and/or refractive object).
    Shader.pass_mat4("matrix2",glGetFloatv(GL_MODELVIEW_MATRIX))
    glPopMatrix()
    
    #Pass the cubemap
    Shader.pass_texture(Cubemap,1)
    Shader.pass_texture(Normalmap,2)
    Shader.pass_bool("using_normalmap",using_normalmap)
    Shader.pass_int("reflect_refract",reflect_refract)
    glPushMatrix()
    glTranslatef(0.0,1.0,0.0)
    spaceship_rotate()
    Spaceship.draw_vbo(Shader)
    glPopMatrix()
    
    glLibUseShader(None)
    Plane.draw()
    draw_env_cube()

    Window.flip()
