#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#LCLICK + DRAG - Rotate spaceship

#Theory:
#For a cartoony look, cel shading can be used.  Cel-shading
#simply converts the rendered object to a few tones, making
#it look like a low-quality print in a comic book or
#something.  Adding an outline increases the "pen-drawn"
#style, and in accomplished by drawing the back-faces of
#the object with a thick line; the object's edges are drawn
#in a thick line.  

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View3D, Spaceship, SpaceshipRotation, Light1, Shader
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,20)

    Spaceship = glLibObject("data/objects/Spaceship.obj",GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    Spaceship.build_vbo()

    SpaceshipRotation = [0,0]

    #Set the clear color to grey so that
    #the spaceship is clearly visible.
    glClearColor(0.3,0.3,0.3,1.0)

    glEnable(GL_LIGHTING)
    Light1 = glLibLight(1)
    Light1.set_pos([0,100,0])
    Light1.enable()

    pygame.mouse.get_rel()

    Shader = glLibShader()
    #This cel shader is quite simple.  It takes the intensity
    #at any given point and divides it into one of three colors.
    #At 3/16 intensity, it's 0.5.  At 8/16 intensity, it's 0.75.
    #otherwise, it's 1.0.  This follows implementations that can
    #Use a 1-D texture.  As of 4/16/2009, the 1-D texture this
    #shader effectively simulates can be found here:
    #http://www.gamedev.net/reference/articles/article1438.asp
    Shader.render_equation("""
    color.rgb += ambient_color.rgb*light_ambient(light1).rgb;
    color.rgb += diffuse_color.rgb*light_diffuse(light1).rgb;
    color.rgb += specular_color.rgb*light_specular_ph(light1).rgb;
    
    float intensity = (color.r + color.g + color.b) / 3.0;
    if (intensity<0.1875) { color.rgb = vec3(0.5); }
    else if (intensity<0.5) { color.rgb = vec3(0.75); }
    else { color.rgb = vec3(1.0); }""")
    errors = Shader.compile()
    
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
    
    #Set the clear color back to black.
    glClearColor(0,0,0,1.0)

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

def draw_spaceship(shader=None):
    glLibUseShader(shader)
    Spaceship.draw_vbo(shader)
def Draw(Window):
    Window.clear()
    View3D.set_view()
    gluLookAt(0,3,3, 0,0,0, 0,1,0)
    Light1.set()

    glRotatef(SpaceshipRotation[0],0,1,0)
    glRotatef(SpaceshipRotation[1],1,0,0)
    glLibUseShader(None)
    #Set the outline's parameters
    glDisable(GL_TEXTURE_2D);glColor3f(0,0,0);glDisable(GL_LIGHTING)
    #Draw the spaceship's outline, with a line width of 4
    glLibOutline(draw_spaceship,4)
    #Disable the outline's parameters
    glEnable(GL_LIGHTING);glColor3f(1,1,1);glEnable(GL_TEXTURE_2D)
    #Draw the spaceship
    draw_spaceship(Shader)

    glLibUseShader(None)

    Window.flip()
