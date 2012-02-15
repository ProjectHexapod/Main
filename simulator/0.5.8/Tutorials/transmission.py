#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#m             - Switch between candle and glass rendering modes
#f             - Toggle using FBO for depthmap updates
#LCLICK + DRAG - Rotate camera
#RCLICK + DRAG - Rotate spaceship
#SROLL WHEEL   - Zoom

#Theory:
#Light is transmitted through some objects, but some of the light is absorbed.
#Assuming that two layers of polygons is an object (one layer in and one layer
#out), the distance between them can be measured, and the light attenuation
#measured.  This is accomplished by depth peeling, which causes multiple depth
#maps to be created, capturing various layers of geometry.  Again, measuring
#the distance between layers determines how much light is absorbed.  If the
#light comes from one direction, the object appears to cast shadows on itself.
#This is the case with mode 1.  If, however, the scene is assumed to be evenly
#lit (light coming from all places), the attenuation can be computed simply by
#measuring the thickness of the material from the camer'a perspective.  So,
#the depth peel is done from the camera's perspective.  This is the case with
#mode 2, which also adds a cubemap to highten the effect.  

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global fbo1_light, fbo2_light, fbo1_screen, fbo2_screen, View3D, View3DDepthRender, LightView, LightViewFBO, CubemapView
    global Spaceship, EnvCube
    global SpaceshipRotation, CameraRotation, CameraRadius, mode, using_fbo
    global Light1
    global DrawShader, DepthPeelShader, DepthPeelShaderSingle
    global FloorTexture, Cubemap
    global number_of_depth_layers, textures
    mode_1_size_direct = 512
    mode_1_size_fbo = 512
    mode_2_size = list(Screen)
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,200.0)
    View3DDepthRender = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,10.0)
    LightView = glLibView3D((0,0,mode_1_size_direct,mode_1_size_direct),90,0.1,3.0)
    LightViewFBO = glLibView3D((0,0,mode_1_size_fbo,mode_1_size_fbo),90,0.1,3.0)
    CubemapView = glLibView3D((0,0,512,512),90)

    Spaceship = glLibObject("data/objects/Spaceship.obj",GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    Spaceship.build_vbo()

    FloorTexture = glLibTexture2D("data/floor.jpg",[0,0,512,512],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    SpaceshipRotation = [0,0]
    CameraRotation = [90,23]
    CameraRadius = 5.0
    mode = 1
    number_of_depth_layers = 8
    using_fbo = False

    if GLLIB_FRAMEBUFFERS_AVAILABLE:
        fbo1_light = glLibFBO((mode_1_size_fbo,mode_1_size_fbo))
        fbo1_light.add_render_target(1,type=GLLIB_DEPTH)
        fbo2_light = glLibFBO((mode_1_size_fbo,mode_1_size_fbo))
        fbo2_light.add_render_target(1,type=GLLIB_DEPTH)
        fbo1_screen = glLibFBO(mode_2_size)
        fbo1_screen.add_render_target(1,type=GLLIB_DEPTH)
        fbo2_screen = glLibFBO(mode_2_size)
        fbo2_screen.add_render_target(1,type=GLLIB_DEPTH)

    glEnable(GL_LIGHTING)
    Light1 = glLibLight(1)
    Light1.set_pos([0,2,1])
    Light1.enable()

    texturenames = []
    for texturename in ["xpos","xneg","ypos","yneg","zpos","zneg"]:
        texturenames.append("data/cubemaps/"+texturename+".jpg")
    textures = []
    for texturename in texturenames:
        texture = glLibTexture2D(texturename,(0,0,256,256),GLLIB_RGB,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
        texture.edge(GLLIB_CLAMP)
        textures.append(texture)
    EnvCube = glLibRectangularSolid([100.0,100.0,100.0],textures)

    Cubemap = glLibTextureCube([None]*6,(0,0,512,512),GLLIB_RGB,GLLIB_FILTER)

    pygame.mouse.get_rel()

    textures = [None]*number_of_depth_layers

    alpha = 32.0
    #"subsurface_absorb8_intensity("""+str(alpha)+""")" samples "8" depthmaps
    #(tex2D_1 through tex2D_8) and adds the differences to get a measure of a
    #depth the light traveled through, and hence the light's intensity.  Using
    #other numbers works too.  Change number_of_depth_layers.  alpha is alpha,
    #the substance's optical density.  The first mode renders the object using
    #a single light source.  The second mode renders the object using an evenly
    #lit scene.  This attenuation model can be found:
    #http://en.wikipedia.org/wiki/Beer%E2%80%93Lambert_law
    DrawShader = glLibShader()
    DrawShader.user_variables("uniform int mode;")
    DrawShader.render_equation("""
    if (mode==1) {
        color.rgb += ambient_color.rgb*light_ambient(light1).rgb;
        color.rgb += diffuse_color.rgb*light_diffuse(light1).rgb;
        color.rgb += specular_color.rgb*light_specular_ph(light1).rgb;
        color.rgb = clamp(color.rgb,0.5,1.0);
        color *= vec4(1.0,1.0,0.5,1.0);
        color.rgb *= absorb"""+str(number_of_depth_layers)+"""_proj("""+str(alpha)+""",
        """+str(LightViewFBO.near)+","+str(LightViewFBO.far)+""");
    }
    else {
        vec3 cubenorm = cubemap_normal();
        vec3 refractsample = cubemap_refract_sample(texCube_9,cubenorm,1.0).rgb;
        float cosincidenceangle = dot(normal,vec3(0.0,0.0,1.0));
        
        float absorption = absorb"""+str(number_of_depth_layers)+"""_point("""+str(alpha)+""",
        """+str(View3DDepthRender.near)+","+str(View3DDepthRender.far)+""",gl_FragCoord.xy/vec2(
        """+str(float(mode_2_size[0]))+","+str(float(mode_2_size[1]))+"""));

        vec3 rgb_atten = vec3(pow(absorption,2.0),absorption,pow(absorption,4.0));
        color.rgb = refractsample*rgb_atten;
    }""")
    DrawShader.max_textures_cube(9)
    errors = DrawShader.compile()
##    if errors != "": pygame.quit();raw_input(errors);sys.exit()
##    print "No errors to report with transmission shader (transmission.py)!"
    print errors

    #Shaders for depth peeling
    DepthPeelShader = glLibShader()
    DepthPeelShader.use_prebuilt(GLLIB_DEPTH_PEEL)

def quit():
    global Light1, Spaceship
    glDisable(GL_LIGHTING)
    del Light1
    del Spaceship

def GetInput():
    global CameraRadius, mode, using_fbo
    mrel = pygame.mouse.get_rel()
    mpress = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT: quit(); pygame.quit(); sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: return False
            elif event.key == K_m: mode = 3-mode
            elif event.key == K_f: using_fbo = not using_fbo
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 5: CameraRadius += .2
            if event.button == 4: CameraRadius -= .2
    if mpress[0]:
        CameraRotation[0] += mrel[0]
        CameraRotation[1] += mrel[1]
    if mpress[2]:
        SpaceshipRotation[0] += mrel[0]
        SpaceshipRotation[1] += mrel[1]

def DrawEnvironment():
    glDisable(GL_LIGHTING)
    EnvCube.draw()
    glEnable(GL_LIGHTING)
def RotateAbsorbingObjects():
    glRotatef(SpaceshipRotation[0],0,1,0)
    glRotatef(SpaceshipRotation[1],1,0,0)
def TransformAbsorbingObjects():
    glTranslatef(0.0,1.0,0.0)
    RotateAbsorbingObjects()
def DrawAbsorbingObjects(shader=None):
    glPushMatrix()
    TransformAbsorbingObjects()
    Spaceship.draw_vbo(shader)
    glPopMatrix()
def Draw(Window):
    global textures
    #Update the cubemap
    if mode == 2:
        glLibSelectTexture(Cubemap)
        glLibUpdateCubeMap([0,1,0],CubemapView,DrawEnvironment)
    
    #Depth peel pass.  Makes a list of depthmaps, each one
    #containing the depth of a different layer of polygons.  
    camerapos = [0 + CameraRadius*cos(radians(CameraRotation[0]))*cos(radians(CameraRotation[1])),
                 1 + CameraRadius*sin(radians(CameraRotation[1])),
                 0 + CameraRadius*sin(radians(CameraRotation[0]))*cos(radians(CameraRotation[1]))]
    if mode == 1: #candle material
        if not using_fbo:
            textures,proj,view = glLibDepthPeel(Light1.get_pos(),LightView,[0,1,0],number_of_depth_layers,\
                                                DepthPeelShader,DrawAbsorbingObjects,\
                                                textures,filtering=GLLIB_FILTER,precision=32)
        else:
            textures,proj,view = glLibDepthPeelFBO(fbo1_light,fbo2_light,Light1.get_pos(),LightViewFBO,[0,1,0],\
                                                   number_of_depth_layers,DepthPeelShader,DrawAbsorbingObjects)
    else: #Non-refractive glass material
        if not using_fbo:
            textures,proj,view = glLibDepthPeel(camerapos,View3DDepthRender,[0,1,0],number_of_depth_layers,\
                                                DepthPeelShader,DrawAbsorbingObjects,\
                                                textures,filtering=GLLIB_FILTER,precision=32)
        else:
            textures,proj,view = glLibDepthPeelFBO(fbo1_screen,fbo2_screen,camerapos,View3DDepthRender,[0,1,0],\
                                                   number_of_depth_layers,DepthPeelShader,DrawAbsorbingObjects)

    Window.clear()
    View3D.set_view()
    gluLookAt(camerapos[0],camerapos[1],camerapos[2], 0,1,0, 0,1,0)
    if mode == 1:
        Light1.set()
        Light1.draw_as_sphere()

    glLibUseShader(DrawShader)
    #Pass the cubemap
    DrawShader.pass_texture(Cubemap,9)
    #Choose the rendering mode
    DrawShader.pass_int("mode",mode)
    #Pass the cubemap matrix (contains the rotations only
    #of the reflective and/or refractive object).
    glPushMatrix()
    glLoadIdentity()
    RotateAbsorbingObjects()
    DrawShader.pass_mat4("matrix2",glGetFloatv(GL_MODELVIEW_MATRIX))
    glPopMatrix()
    glPushMatrix()
    #Send the depthmaps to the shader so they can be used
    glLibDrawWithDepthMaps([textures,proj,view],1,DrawShader,TransformAbsorbingObjects)
    DrawAbsorbingObjects(DrawShader)
    glPopMatrix()

    glLibUseShader(None)
    
    if mode == 2:
        DrawEnvironment()

    Window.flip()
