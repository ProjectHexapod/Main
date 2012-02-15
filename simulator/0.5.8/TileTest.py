import pygame
from pygame.locals import *
import wx
import sys, os
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("TileTest - Ian Mallett")
def ChooseFile():
    wildcard = "All files (*.*)|*.*|.JPG Picture File (*.jpg)|*.jpg|.PNG Picture File (*.png)|*.png|.GIF Picture File (*.gif)|*.gif|.BMP Picture File (*.bmp)|*.bmp|.PCXPicture File (*.pcx)|*.pcx|.TGA Picture File (*.tga)|*.tga|.TIF Picture File (*.tif)|*.tif|.LBM Picture File (*.lbm)|*.lbm|.PBM Picture File (*.pbm)|*.pbm|.PGM Picture File (*.pgm)|*.pgm|.PPM Picture File (*.ppm)|*.ppm|.XPM Picture File (*.xpm)|*.xpm"
    app = wx.PySimpleApp()
    file_picker = wx.FileDialog(None,wildcard=wildcard,style=wx.FD_OPEN)
    file_picker.ShowModal()
    path = file_picker.GetPath()
    app.Destroy()
    if path != "":
        surface = pygame.image.load(path)
        return surface
    else: pygame.quit(); sys.exit()
position = [0,0]
def GetInput():
    global position
    key = pygame.key.get_pressed()
    mpress = pygame.mouse.get_pressed()
    mrel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()
    if key[K_ESCAPE]:
        LoadImage()
    if mpress[0]:
        position[0] += mrel[0]
        position[1] += mrel[1]
        if position[0] >  size[0]: position[0] = 0
        if position[0] < -size[0]: position[0] = 0
        if position[1] >  size[1]: position[1] = 0
        if position[1] < -size[1]: position[1] = 0
def Draw():
    toprow = position[1]-size[1]
    middlerow = position[1]
    bottomrow = position[1]+size[1]
    leftcolumn = position[0]-size[0]
    centrecolumn = position[0]
    rightcolumn = position[0]+size[0]
    for x in [leftcolumn,centrecolumn,rightcolumn]:
        for y in [toprow,middlerow,bottomrow]:
            Surface.blit(surface,(x,y))
    pygame.display.flip()
def LoadImage():
    global surface, Surface, size
    surface = ChooseFile()
    size = surface.get_size()
    Surface = pygame.display.set_mode(size)
    surface.convert()
def main():
    LoadImage()
    while True:
        GetInput()
        Draw()
if __name__ == '__main__': main()
