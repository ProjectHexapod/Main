#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#LCLICK + DRAG - Rotate camera

#Theory:
#glLibShader(...) provides high-level access to shaders, which
#define vertex and fragment operations directly.  Setting "color"
#to red produces a red fragment.  When the spaceship is drawn with
#the shader, the spaceship is red.

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View3D, Spaceship, SpaceshipRotation, Light1, Shader
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,20)

    Spaceship = glLibObject("data/objects/Spaceship.obj",GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    Spaceship.build_vbo()

    SpaceshipRotation = [0,0]

    glEnable(GL_LIGHTING)
    Light1 = glLibLight(1)
    Light1.set_pos([0,100,0])
    Light1.enable()

    pygame.mouse.get_rel()

    #Create a shader instance
    Shader = glLibShader()
    #Set the render equation.  The fragment's color will be set
    #to color.rgba, which, by default, is vec4(0.0,0.0,0.0,1.0).
    #Here, the rgb components of color are set to a red color.  
    Shader.render_equation("color.rgb = vec3(1.0,0.0,0.0);")
    #Compile the shader, returns errors
    errors = Shader.compile()
    
    #Lines 42-47:
    #Check for errors.  It's an excellent idea to have
    #similar code when developing any shader project.  This
    #code stops the program until you can read the errors,
    #then exits the program on ENTER.  Some cards output a
    #"success" string, which this code mistakes for errors.
    #Line 49 replaces it, only printing the error (or
    #success); not reacting to it, but not closing the
    #program in the event of a failure either.
    
##    if errors != "":
##        pygame.quit()
##        raw_input(errors)
##        sys.exit()
##    else:
##        print "No errors to report with red shader (shaderdrawing.py)!"
    
    print errors

def quit():
    global Light1, Spaceship
    glDisable(GL_LIGHTING)
    del Light1
    del Spaceship

def GetInput():
    mrel = pygame.mouse.get_rel()
    mpress = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT: quit(); pygame.quit(); sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE: return False
    if mpress[0]:
        SpaceshipRotation[0] += mrel[0]
        SpaceshipRotation[1] += mrel[1]

def Draw(Window):
    Window.clear()
    View3D.set_view()
    gluLookAt(0,3,5, 0,0,0, 0,1,0)
    Light1.set()

    #Use the shader.  Subsequent draws to the
    #framebuffer will go through the shader.
    #Our shaders draws fragments as red.  We
    #should see a red spaceship when the example
    #is run.  
    glLibUseShader(Shader)
    
    glRotatef(SpaceshipRotation[0],0,1,0)
    glRotatef(SpaceshipRotation[1],1,0,0)
##    Spaceship.draw_arrays()
##    Spaceship.draw_list()
    Spaceship.draw_vbo()
    
    #Use the fixed function pipeline again
    glLibUseShader(None)

    Window.flip()
