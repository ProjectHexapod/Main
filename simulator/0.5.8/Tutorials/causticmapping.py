#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#s             - Toggle spaceship auto-spinning
#r             - switch between refraction and reflection
#o             - Switches among a spaceship object, a torus object, a disco ball, and a ring
#UP            - Rotate light up
#DOWN          - Rotate light down
#CTRL + UP     - Move object up
#CTRL + DOWN   - Move object down
#e + UP        - Increase eta (ratio of refractive indices, means refractive index of spaceship gets small)
#e + DOWN      - Decrease eta (ratio of refractive indices, means refractive index of spaceship gets larger)
#LCLICK + DRAG - Rotate camera
#RCLICK + DRAG - Rotate spaceship
#SROLL WHEEL   - Zoom

#Theory:
#"Caustics" is the name of the patterns of light and dark formed on a surface in the
#presence of reflective and/or refractive objects.  A grid of points (usually
#corresponding to 1 point per pixel) represents light coming from the light source.
#These points are reflected or refracted through the object.  A shadowmap makes the
#area dark (no light transmitted).  If the points pass directly through the object
#(which they do at first, when eta = 1.0) then they should make the area bright
#again.  If the points concentrate, however, in a small space, they make that area
#brighter.  This leaves the other areas untouched, so they are the color of the
#shadowmap; i.e., dark.  

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View2D, View3D, posnorm_fbo1, posnorm_fbo2, caustic_fbo, using_fbo, grid_sc, ShadLightView, CaustLightView, CubemapView
    global causticposmaps, causticnormmaps, causticmap, depthmap, proj, view
    global Spaceship, DiscoBall, Floor, FloorNoTexture, Cylinder, object, EnvCube, CausticGrid, Cubemap
    global ObjectRotation, ObjectPosition
    global CameraRotation, CameraRadius, rotating, rotatingcounter
    global Light1, layers
    global ObjectShader, CausticPhongShader, CausticPositionNormalShader, CausticmapGeneratorShader
    global Normalmap, FloorTexture
    global causticparticlesize, causticparticlebrightness, eta, refraction_reflection
    using_fbo = False
    shadowmapres = 512
    cubemapres = 128
    grid_sc = 0.8
    causticgridres = 512
    causticmapres = 512
    view_angle = 20
    
    causticparticlesize = 3
    causticparticlebrightness = 0.04
##    causticparticlesize = 6
##    causticparticlebrightness = 0.012
##    causticparticlesize = 9
##    causticparticlebrightness = 0.006
    
    View2D = glLibView2D((0,0,Screen[0],Screen[1]))
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,200)
    ShadLightView = glLibView3D((0,0,shadowmapres,shadowmapres),view_angle,7,15)
    CaustLightView = glLibView3D((0,0,causticmapres,causticmapres),view_angle,7,15)
    CubemapView = glLibView3D((0,0,cubemapres,cubemapres),90)

    try:
        posnorm_fbo1 = glLibFBO((causticmapres,causticmapres))
        posnorm_fbo1.add_render_target(1)
        posnorm_fbo1.add_render_target(2)
        posnorm_fbo1.add_render_target(3,type=GLLIB_DEPTH)
        posnorm_fbo2 = glLibFBO((causticmapres,causticmapres))
        posnorm_fbo2.add_render_target(1)
        posnorm_fbo2.add_render_target(2)
        posnorm_fbo2.add_render_target(3,type=GLLIB_DEPTH)
        caustic_fbo = glLibFBO((causticmapres,causticmapres))
        caustic_fbo.add_render_target(1,filter=GLLIB_FILTER)
    except:
        print "FBOs could not be created"

    Spaceship = glLibObject("data/objects/Spaceship.obj",GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    Spaceship.build_vbo()

    DiscoBall = glLibObject("data/objects/disco.obj")
    DiscoBall.build_vbo()

    Cylinder = glLibCylinder(0.3,0.75,0.75,32,cap1=False,cap2=False,normals=GLLIB_VERTEX_NORMALS,normalflip=False,texture=False)

    FloorTexture = glLibTexture2D("data/floor.jpg",[0,0,512,512],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

    Floor = glLibPlane(5,(0,1,0),FloorTexture,10)
    FloorNoTexture = glLibPlane(5,(0,1,0),uv_repeat=10)

    Normalmap = glLibTexture2D("data/rocknormal.png",[0,0,255,255],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)

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
    Cubemap.edge(GLLIB_CLAMP)

    #Prepare the caustics
    glLibPrepareCaustics()
    #Create a grid so that the caustic effects are evenly distributed.  
    CausticGrid = glLibGrid2D(causticgridres)

    ObjectRotation = [0,0]
    ObjectPosition = [0,1.0,0]
    object = 1
    rotating = False
    refraction_reflection = 1
    rotatingcounter = 0.0
    CameraRotation = [90,35]
    CameraRadius = 8.0
    eta = 1.0
    #The number of layers of data that will be processed.  More layers can
    #make more accurate effects--especially when the geometry is complicated,
    #but the reuslt will be slower.  
    layers = 4

    #Just like shadowmapping, update--don't remake--textures for speed.
    causticposmaps = [None]*layers
    causticnormmaps = [None]*layers
    causticmap = None
    depthmap = None
    proj = None
    view = None

    glEnable(GL_LIGHTING)
    Light1 = glLibLight(1)
    #The light mustn't be directly over the object's
    #position (here (0,1,0)) or gluLookAt(...) will not
    #function properly, as the position, center, and up
    #vector will be collinear.
    Light1.set_pos([0,10,0.0001])
    Light1.enable()

    pygame.mouse.get_rel()

    ObjectShader = glLibShader()
    ObjectShader.user_variables("uniform int refraction_reflection;uniform float eta;")
    ObjectShader.render_equation("""
    vec3 cubenorm = vec3(0.0);
    cubenorm = cubemap_normal();
    //cubenorm = cubemap_normal_from_normalmap(tex2D_2,uv);
    cubenorm = normalize(cubenorm);
    vec4 sample = vec4(0.0);
    if (refraction_reflection==1) { sample = cubemap_refract_sample(texCube_1,cubenorm,eta); }
    else                          { sample = cubemap_reflect_sample(texCube_1,cubenorm    ); }
    color.rgb = sample.rgb;
    //color.rgb *= clamp(shadowed(tex2D_3,1.0,false),0.5,1.0);""")
    ObjectShader.uv_transform("uv*=10.0;")
    ObjectShader.max_textures_cube(1)
    errors = ObjectShader.compile()
    print errors
##    if errors != "":pygame.quit();raw_input(errors);sys.exit()
##    print "No errors to report with object drawing shader (causticmapping.py)!"

    #"add_caustic(tex2D_3)" add the caustics to the fragment.
    #If the shaded area does not look correct, change "false"
    #to "true" in this shader.
    CausticPhongShader = glLibShader()
    CausticPhongShader.render_equation("""
    color.rgb += ambient_color.rgb*light_ambient(light1).rgb;
    color.rgb += diffuse_color.rgb*light_diffuse(light1).rgb;
    color.rgb += specular_color.rgb*light_specular_ph(light1).rgb;
    color.rgb *= clamp(shadowed(tex2D_2,1.0,false),0.5,1.0);
    color.rgb += vec3(add_caustics(tex2D_3)*3.0);
    color.rgb *= texture2D(tex2D_1,uv).rgb;""")
    errors = CausticPhongShader.compile()
    print errors
##    if errors != "":pygame.quit();raw_input(errors);sys.exit()
##    print "No errors to report with caustics/Phong shader (causticmapping.py)!"

    #Generates position and normal maps
    CausticPositionNormalShader = glLibShader()
    CausticPositionNormalShader.use_prebuilt(GLLIB_POSITION_MAP,layers)

    #Renders the caustic map
    CausticmapGeneratorShader = glLibShader()
    CausticmapGeneratorShader.use_prebuilt(GLLIB_CAUSTIC_MAP)

def quit():
    global Light1, Spaceship, CausticGrid
    glDisable(GL_LIGHTING)
    del Light1
    del Spaceship
    del CausticGrid

def GetInput():
    global CameraRadius, ObjectRotation, rotating, rotatingcounter, object, refraction_reflection, using_fbo, eta
    global causticposmaps, causticnormmaps
    mrel = pygame.mouse.get_rel()
    mpress = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT: quit(); pygame.quit(); sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE: return False
            elif event.key == K_s: rotating = not rotating
            elif event.key == K_o:
                object += 1
                if object == 5: object = 1
            elif event.key == K_r: refraction_reflection = 3 - refraction_reflection
            elif event.key == K_f:
                using_fbo = not using_fbo
                #Must reset; the contents of causticposmaps and causticnormmaps
                #will be FBO rendertargets, and vice-versa.
                causticposmaps = [None]*layers; causticnormmaps = [None]*layers
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 5: CameraRadius += .2
            if event.button == 4: CameraRadius -= .2
    if mpress[0]:
        CameraRotation[0] += mrel[0]
        CameraRotation[1] += mrel[1]
    if mpress[2]:
        ObjectRotation[0] += mrel[0]
        ObjectRotation[1] += mrel[1]
    if key[K_e]:
        if key[K_UP]: eta += 0.01
        if key[K_DOWN]: eta -= 0.01
        #clamp the refractive index to 1/1 and 1/4, meaning the
        #ship can have a refractive index of any number 1 to 4
        eta = clamp(eta,0.25,1.0)
    elif key[K_LCTRL] or key[K_RCTRL]:
        if key[K_UP]: ObjectPosition[1] += 0.01
        if key[K_DOWN]: ObjectPosition[1] -= 0.01
    else:
        if key[K_UP]:
            position = Light1.get_pos()
            position = rotate_arbitrary_deg(position,[1,0,0],1)
            Light1.set_pos(position)
        if key[K_DOWN]:
            position = Light1.get_pos()
            position = rotate_arbitrary_deg(position,[1,0,0],-1)
            Light1.set_pos(position)
    if rotating:
        ObjectRotation[0] += 1
        ObjectRotation[1] = 45.0*sin(rotatingcounter*2.0*pi)
    ObjectRotation = map(lambda num:num%360.0,ObjectRotation)
    
    rotatingcounter += 0.01
    if rotatingcounter == 1.0:
        rotatingcounter = 0.0

def draw_env_cube():
    #Draws the environment box
    glDisable(GL_LIGHTING)
    EnvCube.draw()
    glEnable(GL_LIGHTING)
def draw_reflectees():
    #Draws everything that should be in the cube map
    Light1.set()
    draw_env_cube()
    draw_floor()
def draw_receivers():
    #Draws the receiver of the caustic map (must have no texture!)
    FloorNoTexture.draw()
def draw_floor():
    #Draws the floor rendered with shadow and caustic maps
    glLibUseShader(CausticPhongShader)
    #not necessary, passed internally by Floor.draw().  Here, for clarity.
    CausticPhongShader.pass_texture(FloorTexture,1)
    if depthmap:
        glLibDrawWithShadowMaps([[depthmap,proj,view]],2,CausticPhongShader,lambda:0)
    if causticmap:
        CausticPhongShader.pass_texture(causticmap,3)
    Floor.draw()
    glLibUseShader(None)
def object_transform():
    #Translates and rotates the object
    glTranslatef(*ObjectPosition)
    object_rotate()
def object_rotate():
    #Applies the rotation transformation to the object
    glRotatef(ObjectRotation[0],0,1,0)
    if object == 1:
        glRotatef(ObjectRotation[1],1,0,0)
    elif object == 2:
        glRotatef(ObjectRotation[1]+90,1,0,0)
    elif object == 3:
        glRotatef(ObjectRotation[1],1,0,0)
    elif object == 4:
        glRotatef(ObjectRotation[1],1,0,0)
def draw_object():
    #Draws the object, passing stuff to ObjectShader
    glPushMatrix()
    object_transform()
    glLibUseShader(ObjectShader)
    ObjectShader.pass_int("refraction_reflection",refraction_reflection)
    if object == 1:
        Spaceship.draw_vbo(ObjectShader)
    elif object == 2:
        glutSolidTorus(0.3,0.5,32,32)
    elif object == 3:
        glPushMatrix()
        glScalef(0.3,0.3,0.3)
        DiscoBall.draw_vbo(ObjectShader)
        glPopMatrix()
    elif object == 4:
        Cylinder.draw()
    glPopMatrix()
def draw_object_simple():
    #Draws the object
    glPushMatrix()
    object_transform()
    if object == 1:
        Spaceship.draw_vbo(withmaterials=False)
    elif object == 2:
        glutSolidTorus(0.3,0.5,32,32)
    elif object == 3:
        glPushMatrix()
        glScalef(0.3,0.3,0.3)
        DiscoBall.draw_vbo()
        glPopMatrix()
    elif object == 4:
        Cylinder.draw()
    glPopMatrix()
def Draw(Window):
    global causticposmaps, causticnormmaps, causticmap, using_causticmap, depthmap, proj, view
    glLibSelectTexture(Cubemap)
    glLibUpdateCubeMap(ObjectPosition,CubemapView,draw_reflectees)

    Window.clear()
    glLibUseShader(None)
    depthmap,proj,view = glLibMakeShadowMap(Light1,ShadLightView,ObjectPosition,depthmap,draw_object_simple,filtering=GLLIB_FILTER)

    #Set up the receiving, refracting, and reflecting draw functions.  If there is more than one layer,
    #none of these must have ANY texture bindings to texture target 1!
    draw_receivers_func = draw_receivers
    if refraction_reflection == 1:
        draw_refractors_func = draw_object_simple
        draw_reflectors_func = lambda:0
    else:
        draw_refractors_func = lambda:0
        draw_reflectors_func = draw_object_simple
    #Generate positionmap and normalmap from the light's perspective (either works, but FBO is much more efficient; using 1/2 as many passes)
    if using_fbo:
        causticposmaps,causticnormmaps = glLibCausticPositionMapFBO(posnorm_fbo1,posnorm_fbo2,Light1,CaustLightView,ObjectPosition,
                                                                    layers,CausticPositionNormalShader,\
                                                                    draw_receivers_func,draw_refractors_func,draw_reflectors_func)
    else:
        causticposmaps,causticnormmaps = glLibCausticPositionMap(Light1,CaustLightView,ObjectPosition,layers,CausticPositionNormalShader,\
                                                                 draw_receivers_func,draw_refractors_func,draw_reflectors_func,\
                                                                 causticposmaps,causticnormmaps,filtering=False,precision=8)
##    print using_fbo,causticposmaps,causticnormmaps

    #Generate causticmap from light's perspective
##    if using_fbo:
##        causticmap = glLibCausticMapFBO(caustic_fbo,CaustLightView,ObjectPosition,CausticmapGeneratorShader,CausticGrid,grid_sc,\
##                                        causticparticlesize,causticparticlebrightness,eta,causticposmaps[:1],causticnormmaps[:1])
##    else:
    if True:
        causticmap = glLibCausticMap(CaustLightView,ObjectPosition,CausticmapGeneratorShader,CausticGrid,grid_sc,causticparticlesize,\
                                     causticparticlebrightness,eta,causticposmaps[:1],causticnormmaps[:1],causticmap,filtering=GLLIB_FILTER)
    
    Window.clear()
    View3D.set_view()
    camerapos = [0 + CameraRadius*cos(radians(CameraRotation[0]))*cos((radians(CameraRotation[1]))),
                 1 + CameraRadius*sin(radians(CameraRotation[1])),
                 0 + CameraRadius*sin(radians(CameraRotation[0]))*cos((radians(CameraRotation[1])))]
    gluLookAt(camerapos[0],camerapos[1],camerapos[2], 0,ObjectPosition[1]/2.0,0, 0,1,0)
    Light1.set()

    glLibUseShader(ObjectShader)

    glPushMatrix()
    glLoadIdentity()
    object_rotate()
    ObjectShader.pass_mat4("matrix2",glGetFloatv(GL_MODELVIEW_MATRIX))
    glPopMatrix()
    
    ObjectShader.pass_texture(Cubemap,1)
    ObjectShader.pass_texture(Normalmap,2)
    ObjectShader.pass_float("eta",eta)
    glLibDrawWithShadowMaps([[depthmap,proj,view]],3,ObjectShader,object_transform)
    glPushMatrix()
    draw_object()
    glPopMatrix()

    glLibUseShader(None)
    
    draw_floor()

    draw_env_cube()

    Light1.draw_as_point(20)

    Window.flip()
