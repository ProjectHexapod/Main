#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#LCLICK + DRAG - Rotate camera
#RCLICK + DRAG - Rotate spaceship
#SROLL WHEEL   - Zoom

#Theory:
#As you should already know, normals are perpendicular vectors
#to a surface, and are the basis for lighting in OpenGL.  Normals
#must be specified at every vertex and/or at every face.  However,
#by storing normals in a texture, normals can be specified for
#many points on a polygon.  This allows for very detailed lighting
#with no extra geometry.  The direction of the normal depends on
#the direction of the texture.  Thus, vectors along the direction
#of the U and V directions of the texture as mapped onto the object,
#called tangent and bitangent (or T and B),  must be supplied.
#This is done automatically by glLibObject(...).  Other objects may
#not look correct because the T and B vectors are not specified.

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View3D, Spaceship, Plane, SpaceshipRotation, CameraRotation, CameraRadius, Light1, Shader, Normalmap, pertubation_level
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,20)

    Spaceship = glLibObject("data/objects/Spaceship.obj",GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    Spaceship.build_vbo()

    ambient,diffuse,specular,shininess = [0.24725,0.1995,0.0745,1.0],[0.75164,0.60648,0.22648,1.0],[0.628281,0.555802,0.366065,1.0],51.2
    
    #Objects loaded from .obj files have their own materials
    #that will overwrite the current material when they are
    #drawn.  Simply calling glLibUseMaterial(GLLIB_MATERIAL_GOLD)
    #before drawing won't work; the spaceship's material itself
    #must be changed.  Any of the following methods will work.
    Spaceship.set_material(GLLIB_MATERIAL_GOLD)
##    Spaceship.set_material([GLLIB_MATERIAL_GOLD,0])
##    Spaceship.set_material([ambient,diffuse,specular,shininess])
##    Spaceship.set_material([[ambient,diffuse,specular,shininess],0])

    FloorTexture = glLibTexture2D("data/floor.jpg",[0,0,512,512],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    try:FloorTexture.anisotropy(GLLIB_MAX)
    except:pass

    Plane = glLibPlane(5,(0,1,0),FloorTexture,10)

    #Load a normalmap
    Normalmap = glLibTexture2D("data/tiles normal.jpg",[0,0,512,512],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    try:Normalmap.anisotropy(GLLIB_MAX)
    except:pass

    SpaceshipRotation = [0,0]
    #Add variables for the camera's rotation and radius
    CameraRotation = [90,23]
    CameraRadius = 5.0
    pertubation_level = 1.0

    glEnable(GL_LIGHTING)
    Light1 = glLibLight(1)
    Light1.set_pos([0,10,0])
    Light1.enable()

    pygame.mouse.get_rel()

    Shader = glLibShader()
    #Adds a uniform (variable that the user can pass directly to the
    #shader.  Below, it is used to mix "normal", which contains the
    #flat normal of general objects with a normal from a normalmap.
    #The normalmap specifies normals for individual points, like a
    #texture.  This allows for much more detailed lighting with no
    #computational cost of extra geometry.  The shader must be passed
    #as an argument to Spaceship.draw_vbo(...), however, or information
    #necessary to correctly use the normalmap would not be available,
    #and this effect would look wrong.  "pertubation_level" is set to
    #the variable pertubation_level--which can be changed in
    #GetInput()--in Draw(...), below.
    Shader.user_variables("uniform float pertubation_level;")
    #Set the normal with normal_from_normalmap(...).  The normalmap
    #is "tex2D_1", so we pass it below in Draw(...).  The ambient,
    #diffuse, and Phong specular of light 1 multiplied
    #by the material's ambient, diffuse, and specular factors are
    #added to color, giving the final fragment's color.  The material
    #is set above to be GLLIB_MATERIAL_GOLD.  The necessary parameters
    #will be set automatically when Spaceship is drawn via
    #Spaceship.draw_vbo(Shader).  The current material will also be
    #restored when the spaceship is done drawing; i.e., the material
    #will be the same both before and after the spaceship is drawn.
    Shader.render_equation("""
    normal = normalize(
                       (1.0-pertubation_level)*normal+
                            pertubation_level *normal_from_normalmap(tex2D_1,uv)
                        );
    color.rgb += ambient_color.rgb*light_ambient(light1).rgb;
    color.rgb += diffuse_color.rgb*light_diffuse(light1).rgb;
    color.rgb += specular_color.rgb*light_specular_ph(light1).rgb;""")
    #The normalmap is tileable.  Let's tile it.
    Shader.uv_transform("uv *= vec2(5.0,4.0);")
    errors = Shader.compile()
    print errors
##    if errors != "":
##        pygame.quit()
##        raw_input(errors)
##        sys.exit()
##    else:
##        print "No errors to report with normalmapping shader (normalmapping.py)!"

def quit():
    global Light1, Spaceship
    glDisable(GL_LIGHTING)
    del Light1
    del Spaceship

def GetInput():
    global CameraRadius, pertubation_level
    mrel = pygame.mouse.get_rel()
    mpress = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT: quit(); pygame.quit(); sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE: return False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 5: CameraRadius += .2
            if event.button == 4: CameraRadius -= .2
    #If the left mouse button is clicked,
    #rotate the camera.  Rotate the spaceship
    #if the right mouse button is pressed.
    if mpress[0]:
        CameraRotation[0] += mrel[0]
        CameraRotation[1] += mrel[1]
    if mpress[2]:
        SpaceshipRotation[0] += mrel[0]
        SpaceshipRotation[1] += mrel[1]
    #If up or down is pressed, change the
    #amount of each type of normal that is
    #used.
    if key[K_UP]:
        if pertubation_level < 1.0:
            pertubation_level += 0.04
    if key[K_DOWN]:
        if pertubation_level > 0.0:
            pertubation_level -= 0.04

def Draw(Window):
    Window.clear()
    View3D.set_view()
    #Calculate the camera's position using CameraRotation.
    #Basically just spherical coordinates.
    camerapos = [0 + CameraRadius*cos(radians(CameraRotation[0]))*cos((radians(CameraRotation[1]))),
                 1 + CameraRadius*sin((radians(CameraRotation[1]))),
                 0 + CameraRadius*sin(radians(CameraRotation[0]))*cos((radians(CameraRotation[1])))]
    gluLookAt(camerapos[0],camerapos[1],camerapos[2], 0,1,0, 0,1,0)
    Light1.set()

    glLibUseShader(Shader)
    #Pass the normalmap texture to the shader.  The
    #second argument is 1, so the texture will be
    #available in the shader as "tex2D_1" (because
    #the final argument is 1).
    Shader.pass_texture(Normalmap,1)
    #Pass the mixing coefficient.  See the note above.
    Shader.pass_float("pertubation_level",pertubation_level)

    #Save the current matrix
    glPushMatrix()
    #Raise the spaceship 1 unit up
    glTranslatef(0.0,1.0,0.0)
    glRotatef(SpaceshipRotation[0],0,1,0)
    glRotatef(SpaceshipRotation[1],1,0,0)
    #Pass the optional "shader" argument to .draw_vbo(shader=None)
    #so that vertex tangents will be passed and normalmapping will
    #work as expected.  
    Spaceship.draw_vbo(Shader)
    #Restore the matrix to before it was
    #transformed after glPushMatrix()
    glPopMatrix()
    
    glLibUseShader(None)
    #Draw the floor
    Plane.draw()

    Window.flip()
