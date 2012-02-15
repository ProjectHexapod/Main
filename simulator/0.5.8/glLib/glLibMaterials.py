from glLibLocals import *
def glLibGetMaterialParam(material):
    #Metals
    if   material == GLLIB_MATERIAL_BRASS:
        material_parameters = ([0.329412,0.223529,0.027451],[0.780392,0.568627,0.113725],[0.992157,0.941176,0.807843],27.89743616)
    elif material == GLLIB_MATERIAL_BRONZE:
        material_parameters = ([0.2125,0.1275,0.054],[0.714,0.4284,0.18144],[0.393548,0.271906,0.166721],25.6)
    elif material == GLLIB_MATERIAL_CHROME:
        material_parameters = ([0.25,0.25,0.25],[0.4,0.4,0.4],[0.774597,0.774597,0.774597],76.8)
    elif material == GLLIB_MATERIAL_COPPER:
        material_parameters = ([0.19125,0.0735,0.0225,1.0],[0.7038,0.27048,0.0828,1.0],[0.256777,0.137622,0.086014,1.0],12.8)
    elif material == GLLIB_MATERIAL_GOLD:
        material_parameters = ([0.24725,0.1995,0.0745,1.0],[0.75164,0.60648,0.22648,1.0],[0.628281,0.555802,0.366065,1.0],51.2)
    elif material == GLLIB_MATERIAL_SILVER:
        material_parameters = ([0.19225,0.19225,0.19225,1.0],[0.50754,0.50754,0.50754,1.0],[0.508273,0.508273,0.508273,1.0],51.2)
    #Plastics
    elif material == GLLIB_MATERIAL_BLACK_PLASTIC:
        material_parameters = ([0,0,0,1],[0.01,0.01,0.01,1],[0.50,0.50,0.50,1],32)
    elif material == GLLIB_MATERIAL_CYAN_PLASTIC:
        material_parameters = ([0.0,0.1,0.06],[0.0,0.50980392,0.50980392],[0.50196078,0.50196078,0.50196078],32)
    elif material == GLLIB_MATERIAL_GREEN_PLASTIC:
        material_parameters = ([0.0,0.0,0.0],[0.1,0.35,0.1],[0.45,0.55,0.45],32)
    elif material == GLLIB_MATERIAL_RED_PLASTIC:
        material_parameters = ([0.0,0.0,0.0],[0.5,0.0,0.0],[0.7,0.6,0.6],32)
    elif material == GLLIB_MATERIAL_WHITE_PLASTIC:
        material_parameters = ([0.0,0.0,0.0],[0.55,0.55,0.55],[0.70,0.70,0.70],32)
    elif material == GLLIB_MATERIAL_YELLOW_PLASTIC:
        material_parameters = ([0.0,0.0,0.0],[0.5,0.5,0.0],[0.60,0.60,0.50],32)
    #Rubbers
    elif material == GLLIB_MATERIAL_BLACK_RUBBER:
        material_parameters = ([0.02,0.02,0.02],[0.01,0.01,0.01],[0.4,0.4,0.4],10)
    elif material == GLLIB_MATERIAL_CYAN_RUBBER:
        material_parameters = ([0.0,0.05,0.05],[0.4,0.5,0.5],[0.04,0.7,0.7],10)
    elif material == GLLIB_MATERIAL_GREEN_RUBBER:
        material_parameters = ([0.0,0.05,0.0],[0.4,0.5,0.4],[0.04,0.7,0.04],10)
    elif material == GLLIB_MATERIAL_RED_RUBBER:
        material_parameters = ([0.05,0.0,0.0],[0.5,0.4,0.4],[0.7,0.04,0.04],10)
    elif material == GLLIB_MATERIAL_WHITE_RUBBER:
        material_parameters = ([0.05,0.05,0.05],[0.5,0.5,0.5],[0.7,0.7,0.7],10)
    elif material == GLLIB_MATERIAL_YELLOW_RUBBER:
        material_parameters = ([0.05,0.05,0.0],[0.5,0.5,0.4],[0.7,0.7,0.04],10)
    #Stones (precious, semi-precious, and non-precious)
##    elif material == GLLIB_MATERIAL_EMERALD:
##        material_parameters = ([0.0215,0.1745,0.0215],[0.07568,0.61424,0.07568],[0.633,0.727811,0.633],76.8)
##    elif material == GLLIB_MATERIAL_JADE:
##        material_parameters = ([0.135,0.2225,0.1575,0.95],[0.54,0.89,0.63,0.95],[0.316228,0.316228,0.316228,0.95],12.8)
##    elif material == GLLIB_MATERIAL_OBSIDIAN:
##        material_parameters = ([0.05375,0.05,0.06625,0.82],[0.18275,0.17,0.22252,0.82],[0.332741,0.328634,0.346435,0.82],38.4)
##    elif material == GLLIB_MATERIAL_PEARL:
##        material_parameters = ([0.25,0.20725,0.20725],[1,0.829,0.829],[0.296648,0.296648,0.296648],11.264)
##    elif material == GLLIB_MATERIAL_RUBY:
##        material_parameters = ([0.1745,0.01175,0.01175],[0.61424,0.04136,0.04136],[0.727811,0.626959,0.626959],76.8)
##    elif material == GLLIB_MATERIAL_TURQUOISE:
##        material_parameters = ([0.1,0.18725,0.1745],[0.396,0.74151,0.69102],[0.297254,0.30829,0.306678],12.8)
##    #Made Up
##    elif material == "Super Specular Gold":
##        material_parameters = ([0.0,0.0,0.0,1.0],[0.75164,0.60648,0.22648,1.0],[1.0,1.0,1.0,1.0],64)
    #Misc.
    elif material == GLLIB_MATERIAL_DEFAULT:
        material_parameters = ([0.2,0.2,0.2,1.0],[0.8,0.8,0.8,1.0],[0,0,0,1],0)
##    elif material == GLLIB_GLASS:
##        material_parameters = ([0,0,0,0],[0,0,0,0],[1,1,1,1],32)
##    elif material == GLLIB_NONE:
##        material_parameters = ([0,0,0,0],[0,0,0,0],[0,0,0,0],32)
    elif material == GLLIB_MATERIAL_FULL:
        material_parameters = ([1,1,1,1],[1,1,1,1],[1,1,1,1],128)
#[0.2,0.2,0.2,1.0],[0.8,0.8,0.4,1.0],[1,1,1,1],[0,0,0,1],128
#http://www.sc.ehu.es/ccwgamoa/docencia/Material/OpenGL/Materials-Parameters/MaterialsParameters.htm
#http://devernay.free.fr/cours/opengl/materials.html google "opengl materials"
    return material_parameters
def glLibUseMaterial(material):
    material_parameters = glLibGetMaterialParam(material)
    glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT,  material_parameters[0])
    glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,  material_parameters[1])
    glMaterialfv(GL_FRONT_AND_BACK,GL_SPECULAR, material_parameters[2])
##    glMaterialfv(GL_FRONT_AND_BACK,GL_EMISSION, material_parameters[3])
    glMaterialfv(GL_FRONT_AND_BACK,GL_SHININESS,material_parameters[3])
