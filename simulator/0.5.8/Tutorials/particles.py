#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#p             - Toggles pausing the simulation (toggles updating)
#r             - Toggles auto-rotation
#LCLICK + DRAG - Rotate camera
#SROLL WHEEL   - Zoom

#Theory:
#Particle systems are really neat--but they're tricky.  Built-in to
#OpenGL Library is a GPU particle implementation.  The particles are
#updated and drawn through high-precision textures.  Because most of
#the work is done by the GPU, hundreds of thousands of particles are
#practical.  

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View2D, View3D, Spaceship, Plane, CameraRotation, CameraRadius, Light1, ParticleSystem, ColorRampShader
    View2D = glLibView2D((0,0,Screen[0],Screen[1]))
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,20)

    CameraRotation = [135,23]
    CameraRadius = 5.0

    particle_system = 1
    
    #Create a particle system
    if   particle_system == 1: ParticleSystem = glLibParticleSystem(128**2,32)
    elif particle_system == 2: ParticleSystem = glLibParticleSystem(32**2,32)
    #Parameters
    #   Set the particle system's origin within the box
    ParticleSystem.set_origin([0.0,0.0,0.0])
    #   Set the initial speed of every particle (here up)
    ParticleSystem.set_initial_speed([0.0,0.025,0.0])
    #   Set the force on the particles (here gravity)
    ParticleSystem.set_forces([0.0,-0.005,0.0])
    #   Set the particle system's scalar
    ParticleSystem.set_scale([5.0,0.75,5.0])
    #   Set the particle system's location
    ParticleSystem.set_trans([0.0,0.0,0.0])
    #   Set the rate at which particles are born
    ParticleSystem.set_density(1)
    #   Use to set a bounce coefficient for when the
    #   particles reach the edge of their box.
    bounce = -0.5
    ParticleSystem.set_edge(bounce,bounce,bounce,bounce,bounce,bounce)
    #   Scale the jitter of the particle system
    ParticleSystem.set_jitter([0.01,0.1,0.01])
    #   The rate at which the particles' color fades.
    ParticleSystem.set_fade(0.1)
    #   Set the particles' size.  Default is 100.0.  The size
    #   attenuates with distance and will eventually become
    #   invisible.  
    if   particle_system == 1: ParticleSystem.set_particle_size(100.0)
    elif particle_system == 2: ParticleSystem.set_particle_size(1000.0)
    #   Change the image the particles use
##    ParticleSystem.point_texture = whatever texture you want.
    #   Make the particles filtered and mipmapped (by default, they're not).
    ParticleSystem.point_texture.filtering(GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    glEnable(GL_LIGHTING)
    Light1 = glLibLight(1)
    Light1.set_pos([0,10,0])
    Light1.enable()

    ColorRampShader = glLibShader()
    #Enable for a really fake looking heat wave effect
##    ColorRampShader.user_variables("uniform float time;")
##    ColorRampShader.uv_transform("""
##    uv.x += 0.001*sin((time+uv.y)*360.0);
##    """)
    ColorRampShader.render_equation("""
    vec3 sample = texture2D(tex2D_1,uv).rgb;
    float intensity = sample.r*3.0;
    color.rgb = clamp(vec3(intensity,intensity-1.0,intensity-2.0),0.0,1.0); //intense fire
    //color.rgb = clamp(vec3(intensity,intensity-0.5,intensity-1.5),0.0,1.0); //less intense fire
    //color.rgb = clamp(vec3(intensity-2.0,intensity-1.0,intensity),0.0,1.0); //blue flame
    //color.rgb = intensity*vec3(1.0); //straight white""")
    errors = ColorRampShader.compile()
    print errors
##    if errors != "": pygame.quit();raw_input(errors);sys.exit()
##    print "No errors to report with color ramp shader (particles.py)!"

    pygame.mouse.get_rel()

def quit():
    global Light1, ParticleSystem
    glDisable(GL_LIGHTING)
    del Light1
    del ParticleSystem

paused = False
rotating = False
time = 0.0
def GetInput():
    global CameraRadius, paused, rotating, time
    mrel = pygame.mouse.get_rel()
    mpress = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT: quit(); pygame.quit(); sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: return False
            #If p has been pressed, toggle pausing the
            #particle system (just doesn't update it)
            elif event.key == K_p: paused = not paused
            #If r has been pressed, toggle rotation
            #of the camera around the y axis.  
            elif event.key == K_r: rotating = not rotating
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 5: CameraRadius += .2
            if event.button == 4: CameraRadius -= .2
    if mpress[0]:
        CameraRotation[0] += mrel[0]
        CameraRotation[1] += mrel[1]
    if rotating:
        CameraRotation[0] += 0.5
    #For heat wave effect
    time += 0.0005
    if time == 1.0: time = 0.0
scenemap = None
def Draw(Window):
    global scenemap
    Window.clear()
    View3D.set_view()
    camerapos = [CameraRadius*cos(radians(CameraRotation[0]))*cos((radians(CameraRotation[1]))),
                 CameraRadius*sin((radians(CameraRotation[1]))),
                 CameraRadius*sin(radians(CameraRotation[0]))*cos((radians(CameraRotation[1])))]
    gluLookAt(camerapos[0],camerapos[1],camerapos[2], 0,0,0, 0,1,0)
    Light1.set()

    if not paused:
        ParticleSystem.update()
    
    glLibUseShader(None)
    #Draw the floor
##    Plane.draw()

    ParticleSystem.draw()

    scenemap = glLibSceneToTexture(View3D.rect,scenemap)
    
    Window.clear()
    View2D.set_view()
    glLibUseShader(ColorRampShader)
    ColorRampShader.pass_texture(scenemap,1)
    ColorRampShader.pass_float("time",time)
    glLibTexFullScreenQuad()
    glLibUseShader(None)
    
    Window.flip()

##    raw_input()
