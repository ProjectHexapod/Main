#IMPORTANT:
#THIS ITSELF IS NOT A TUTORIAL; IT IS CODE THAT ALLOWS YOU TO VIEW TUTORIALS.
#THE TUTORIALS ARE AVAILABLE IN Tutorials/ IN THE MAIN DIRECTORY.  SEE
#TUTORIAL 1 (objload.py) FOR MORE INFORMATION.

from glLib import *
sys.path.append("Tutorials")
import objload
import rawload
import shaderdrawing
import basiclighting
import texturetechniques
import normalmapping
import parallaxmapping
import shadowmapping
import cubemapping
import causticmapping
import transmission
import framebuffer
import filters
import particles
import celshading
import cloth

Screen = (800,600)
#Adjusting multisampling makes everything look nicer--except transmission, which breaks
Window = glLibWindow(Screen,caption="OpenGL Library Demo/Tutorials",multisample=False,position=GLLIB_CENTER,vsync=False)

version = glLibGetVersion()
print "OpenGL Library version ",version[0]
print "PyOpenGL version       ",version[1]
print "OpenGL version         ",version[2]

RunningDemo = False

View2D = glLibView2D((0,0,Screen[0],Screen[1]))

BackgroundTexture = glLibTexture2D("data/DemoBackground.png",[0,0,800,600],GLLIB_RGB)
buttonsize = (175,48)
hbuttonsize = (buttonsize[0]/2,buttonsize[1]/2)
buttonrect = (0,0,buttonsize[0],buttonsize[1])
buttonsurf = pygame.Surface(buttonsize).convert_alpha()
pygame.draw.rect(buttonsurf,(255,255,255),buttonrect,1)

Font = pygame.font.SysFont("Times New Roman",16)

Buttons = []
class Button:
    def __init__(self,pos,text,demo):
        self.pos = pos
        self.hovering = False
        self.surf = buttonsurf.copy()
        self.surfhover = buttonsurf.copy()
        self.text = text
        self.surftext = Font.render(text,True,(255,255,255))
        self.surftexthover = Font.render(text,True,(255,255,0))
        self.surf.blit(self.surftext,(hbuttonsize[0]-(self.surftext.get_width()/2),hbuttonsize[1]-(self.surftext.get_height()/2)))
        self.surfhover.blit(self.surftexthover,(hbuttonsize[0]-(self.surftexthover.get_width()/2),hbuttonsize[1]-(self.surftexthover.get_height()/2)))
        self.texture = glLibTexture2D(self.surf,buttonrect,GLLIB_RGBA)
        self.texturehover = glLibTexture2D(self.surfhover,buttonrect,GLLIB_RGBA)
        self.list = glLibQuad(buttonrect,self.texture)
        self.listhover = glLibQuad(buttonrect,self.texturehover)
        self.demo = demo
    def draw(self):
        glTranslatef(self.pos[0],self.pos[1],0)
        if self.hovering: self.listhover.draw()
        else:             self.list.draw()
        glTranslatef(-self.pos[0],-self.pos[1],0)
columns = 3
rows = 6
buttons_param = [["Objects .obj",objload],
                 ["Objects .raw",rawload],
                 ["Shader Drawing",shaderdrawing],
                 ["Basic Lighting",basiclighting],
                 ["Texture Techniques",texturetechniques],
                 ["Normal Mapping",normalmapping],
                 ["Parallax Mapping",parallaxmapping],
                 ["Shadow Mapping",shadowmapping],
                 ["Framebuffer",framebuffer],
                 ["Cube Mapping",cubemapping],
                 ["Transmission",transmission],
                 ["Caustic Mapping",causticmapping],
                 ["Filters",filters],
                 ["Cel Shading",celshading],
                 ["Particles",particles],
                 ["GPU Cloth",cloth]]
xspace = float(Screen[0])/(columns+1.0)
yspace = float(Screen[1])/(rows+1.0)
position = [xspace,Screen[1]-yspace]
index = 0
for column in xrange(columns):
    position[1] = Screen[1]-yspace
    for row in xrange(rows):
        if len(buttons_param) > index:
            button_param = buttons_param[index]
            buttonpos = [position[0]-(buttonsize[0]/2.0),position[1]-(buttonsize[1]/2.0)]
            Buttons.append(Button(map(rndint,buttonpos),str(index+1)+": "+button_param[0],button_param[1]))
        index += 1
        position[1] -= yspace
    position[0] += xspace
    
def quit(): pygame.quit(); sys.exit()

def GetInput():
    global RunningDemo, Demo
    if not RunningDemo:
        mpos = list(pygame.mouse.get_pos())
        mpos[1] = Screen[1]-mpos[1]
        for event in pygame.event.get():
            if event.type == QUIT: quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: quit()
            if event.type == MOUSEBUTTONDOWN:
                for b in Buttons:
                    if b.hovering:
                        RunningDemo = True
                        Demo = b.demo
                        Demo.init(Screen)
                        Window.set_caption("OpenGL Library Demo/Tutorials: "+b.text.split(": ")[1])
        for b in Buttons:
            b.hovering = False
            if mpos[0] > b.pos[0] and mpos[0] < b.pos[0]+buttonsize[0]:
                if mpos[1] > b.pos[1] and mpos[1] < b.pos[1]+buttonsize[1]:
                    b.hovering = True
    else:
        if Demo.GetInput()==False:
            Demo.quit()
            RunningDemo = False
            Window.set_caption("OpenGL Library Demo/Tutorials")
def Draw():
    if not RunningDemo:
        Window.clear()
        View2D.set_view()
        glLibSelectTexture(BackgroundTexture)
        glLibTexFullScreenQuad()
        glLibAlpha(0.3)
        glTranslatef(0,0,0.1)
        for b in Buttons: b.draw()
        glLibAlpha(1.0)
        Window.flip()
    else:
        Demo.Draw(Window)

def main():
    Clock = pygame.time.Clock()
    while True:
        GetInput()
        Draw()
        Clock.tick(60)
##        Clock.tick()
##        print "fps: %f" % round(Clock.get_fps(),2)
if __name__ == '__main__':
    glLibTestErrors(main)
