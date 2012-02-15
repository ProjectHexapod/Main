import pygame
import sys
from math import *
import wx
pygame.init()
def ChooseFile():
    global source_path
    wildcard = "All files (*.*)|*.*|.JPG Picture File (*.jpg)|*.jpg|.PNG Picture File (*.png)|*.png|.GIF Picture File (*.gif)|*.gif|.BMP Picture File (*.bmp)|*.bmp|.PCXPicture File (*.pcx)|*.pcx|.TGA Picture File (*.tga)|*.tga|.TIF Picture File (*.tif)|*.tif|.LBM Picture File (*.lbm)|*.lbm|.PBM Picture File (*.pbm)|*.pbm|.PGM Picture File (*.pgm)|*.pgm|.PPM Picture File (*.ppm)|*.ppm|.XPM Picture File (*.xpm)|*.xpm"
    app = wx.PySimpleApp()
    file_picker = wx.FileDialog(None,wildcard=wildcard,style=wx.FD_OPEN)
    file_picker.ShowModal()
    source_path = file_picker.GetPath()
    app.Destroy()
    if source_path != "":
        surface = pygame.image.load(source_path)
        return surface
    else: pygame.quit(); sys.exit()
surface = ChooseFile()
size = surface.get_size()
surface2 = pygame.Surface(size) #greyscale
surface3 = pygame.Surface([size[0]-1,size[1]-1]) #normal map
for x in xrange(size[0]):
    for y in xrange(size[1]):
        color = surface.get_at((x,y))
        surface2.set_at((x,y),[(color[0]+color[1]+color[2])/3]*3)
xdifferences = []
ydifferences = []
maxdiff = 0
for x in xrange(size[0]-1):
    xdiffrow = []
    ydiffrow = []
    for y in xrange(size[1]-1):
        color_tl = surface2.get_at((x,  y  ))[0]
        color_tr = surface2.get_at((x+1,y  ))[0]
        color_bl = surface2.get_at((x,  y+1))[0]
        color_br = surface2.get_at((x+1,y+1))[0]
        xdiff = (((color_tl+color_bl)/2.0)-((color_tr+color_br)/2.0))
        ydiff = (((color_br+color_bl)/2.0)-((color_tr+color_tl)/2.0))
        if maxdiff < abs(xdiff): maxdiff = abs(xdiff)
        if maxdiff < abs(ydiff): maxdiff = abs(ydiff)
        xdiffrow.append(xdiff)
        ydiffrow.append(ydiff)
    xdifferences.append(xdiffrow)
    ydifferences.append(ydiffrow)
scalar = 128.0/maxdiff
for diffrowindex in xrange(len(xdifferences)):
    for differenceindex in xrange(len(xdifferences[0])):
        xdiff = xdifferences[diffrowindex][differenceindex]
        ydiff = ydifferences[diffrowindex][differenceindex]
        #256 = sqrt(x**2 + y**2 + z**2)
        #z = sqrt(65536 - y**2 - x**2)
        xdiff *= scalar
        ydiff *= scalar
        vector = [xdiff,ydiff,sqrt(65536-(xdiff**2)-(ydiff**2))]
        length = hypot(hypot(vector[0],vector[1]),vector[2])
        vector = [vector[0]/length,vector[1]/length,vector[2]/length]
        vector = [255*vector[0],255*vector[1],255*vector[2]]
        vector = [int(round(127.5+vector[0])),int(round(127.5+vector[1])),int(round(vector[2]))]
        surface3.set_at((diffrowindex,differenceindex),vector)
path = ""
try:
    directories = source_path.split("\\")
    for directory in directories[:-1]:
        path += directory
        path += "\\"
except:pass
pygame.image.save(surface3,path+"normalmap.png")
