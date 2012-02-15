#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#LCLICK + DRAG - Rotate camera
#SROLL WHEEL   - Zoom

#Theory:
#Lighting makes objects look 3D.  glLibLight(...) provides
#high level access to spotlighting, attenuation, and other
#light functions.  Using these features with a shader is
#shown.

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View3D, Plane, CameraRotation, CameraRadius, Light1, Light2, Light3, Light4, Shader, Normalmap
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,20)

    FloorTexture = glLibTexture2D("data/floor.jpg",[0,0,512,512],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    #A plane of size 5, with a normal facing straight up
    #i.e., the XZ plane, textured with "FloorTexture",
    #the latter being tiled 10 times.
    Plane = glLibPlane(5,(0,1,0),FloorTexture,10)

    #Add variables for the camera's rotation and radius
    CameraRotation = [90,23]
    CameraRadius = 8.0

    #Enable lighting.  This is required for fixed function
    #lighting, but as the lighting equation is specified
    #explicitly in the shader, it is not required.  Generally,
    #however, one leaves it on.
    glEnable(GL_LIGHTING)
    
    #Make a light object
    Light1 = glLibLight(1)
    #Set the light's position
    Light1.set_pos([0,1.8,0])
    #Make it a point light (as opposed to directional)
    Light1.set_type(GLLIB_POINT_LIGHT)
    #Set the light's attenuation by changing the three
    #constants in the denominator of the attenuation function.
    #Here, the function is:
    #1.0 / (1.0 + 0.0*dist + 1.0*dist*dist)
    Light1.set_atten(1.0,0.0,1.0)
    #Enable the light.  Again, not strictly necessary for
    #the programmable pipeline.  Required for fixed function.
    Light1.enable()

    Light2 = glLibLight(2)
    Light2.set_pos([2,0.1,0])
    Light2.set_type(GLLIB_POINT_LIGHT)
    #The default diffuse and specular for the first light
    #are both [1,1,1].  However, they are both [0,0,0] for
    #subsequent lights, so we must set them here, while we
    #didn't for Light1.  See the OpenGL documentation.  Let's
    #make them red while we're at it.
    Light2.set_diffuse([0,0,1])
    Light2.set_specular([0,0,1])
    Light2.set_atten(1.0,0.0,1.0)
    Light2.enable()

    Light3 = glLibLight(3)
    Light3.set_pos([-2,1.0,-2.5])
    Light3.set_type(GLLIB_POINT_LIGHT)
    Light3.set_diffuse([0,1,0])
    Light3.set_specular([0,1,0])
    Light3.set_atten(1.0,0.0,1.0)
    #Make a spotlight.  Note the light_spot(...) requirement
    #in the shader below.  First, set the direction as a
    #normalized vector.  Then, make the spotlight have an
    #angle of 10 degrees (default 180; not a spotlight).
    #Then make the exponent of the spotlight.  The result is
    #a green light that projects a cone that, because it is
    #tilted, intersects the plane in an ellipse with softened
    #edges.
    Light3.set_spot_dir(normalize([0.2,-1.0,1.0]))
    Light3.set_spot_angle(45.0)
    Light3.set_spot_ex(0.5)
    Light3.enable()

    Light4 = glLibLight(4)
    Light4.set_pos([-0.5,1.0,-2.5])
    Light4.set_type(GLLIB_POINT_LIGHT)
    Light4.set_diffuse([1,0,0])
    Light4.set_specular([1,0,0])
    Light4.set_atten(1.0,0.0,1.0)
    Light4.set_spot_dir(normalize([-0.4,-1.0,1.0]))
    Light4.set_spot_angle(45.0)
    Light4.set_spot_ex(0.5)
    Light4.enable()

    pygame.mouse.get_rel()

    #Normal OpenGL lighting is per-vertex, meaning that the
    #lighting is calculated at every vertex only and interpolated
    #across each polygon.  Because that looks weird sometimes,
    #this shader implement per-pixel lighting, which evaluates
    #lighting at every fragment.  The floor is a single
    #quadrilateral, so without shaders, there would be a simple
    #gradient across the whole floor, with little discernable
    #pattern--dull indeed!  Shaders to the rescue!
    Shader = glLibShader()
    #light_ambient(light1) takes the ambient component of Light1
    #light_diffuse(light1) takes the diffuse component of Light1
    #light_specular_ph(light1) takes the phong specular component
    #of Light1
    #light_att(light1) takes the attenuation of Light1
    #light_spot returns the intensity of the light due to it's
    #being in a spot or not
    #Multiply the ambient by ambient color, diffuse by diffuse
    #color, specular by specular color and add to color
    Shader.render_equation("""
    vec3 ambient_light = light_ambient(light1).rgb+
                         light_ambient(light2).rgb+
                         light_ambient(light3).rgb+
                         light_ambient(light4).rgb;
    
    vec3 diffuse_light = light_diffuse(light1).rgb*light_att(light1)+
                         light_diffuse(light2).rgb*light_att(light2)+
                     2.0*light_diffuse(light3).rgb*light_att(light3)*light_spot(light3)+
                     2.0*light_diffuse(light4).rgb*light_att(light4)*light_spot(light4);
                         
    vec3 specular_light = light_specular_ph(light1).rgb*light_att(light1)+
                          light_specular_ph(light2).rgb*light_att(light2)+
                      2.0*light_specular_ph(light3).rgb*light_att(light3)*light_spot(light3)+
                      2.0*light_specular_ph(light4).rgb*light_att(light4)*light_spot(light4);
                          
    color.rgb += ambient_color.rgb*ambient_light;
    color.rgb += diffuse_color.rgb*diffuse_light;
    color.rgb += specular_color.rgb*specular_light;""")
    errors = Shader.compile()
    print errors
##    if errors != "":
##        pygame.quit()
##        raw_input(errors)
##        sys.exit()
##    else:
##        print "No errors to report with normalmapping shader (basiclighting.py)!"

def quit():
    global Light1, Light2, Light3, Light4
    glDisable(GL_LIGHTING)
    del Light1, Light2, Light3, Light4

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
    #If the left mouse button is clicked,
    #rotate the camera.  
    if mpress[0]:
        CameraRotation[0] += mrel[0]
        CameraRotation[1] += mrel[1]

def SetCamera():
    gluLookAt(camerapos[0],camerapos[1],camerapos[2], 0,0,0, 0,1,0)
def Draw(Window):
    global camerapos
    Window.clear()
    View3D.set_view()
    #Calculate the camera's position using CameraRotation.
    #Basically just spherical coordinates.
    camerapos = [0 + CameraRadius*cos(radians(CameraRotation[0]))*cos((radians(CameraRotation[1]))),
                 0 + CameraRadius*sin((radians(CameraRotation[1]))),
                 0 + CameraRadius*sin(radians(CameraRotation[0]))*cos((radians(CameraRotation[1])))]
    SetCamera()
    Light1.set()
    Light2.set()
    Light3.set()
    Light4.set()
    
    #Draw the floor
    #   Use the shader
    glLibUseShader(Shader)
    #   Save the current material, and then use
    #   a material that maximizes all parameters
    #   Then, lower the specular exponent to
    #   simulate a less shiny surface.
    glPushAttrib(GL_LIGHTING_BIT)
    glLibUseMaterial(GLLIB_MATERIAL_FULL)
    glMaterialf(GL_FRONT_AND_BACK,GL_SHININESS,5.0)
    #   Light3 and Light4 are spot light1, so we must
    #   send some extra data to the shader to do spot-
    #   lighting correctly.
    glLibSendTransform(Shader,lambda:0)
    glLibSendInvView(Shader,SetCamera)
    #   Draw the plane
    Plane.draw()
    #   Restore the default material
    glPopAttrib()
    #   Use the fixed function pipeline again
    glLibUseShader(None)

    #Draw the lights as points
    for light in [Light1,Light2,Light3,Light4]:
        light.draw_as_point()

    Window.flip()
