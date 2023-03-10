import pygame
import sys

pygame.init()

size = [700, 450]
screen = pygame.display.set_mode(size)

title = "pyUNO"
pygame.display.set_caption(title)

width = screen.get_width()
height = screen.get_height()

colorWhite = (255, 255, 255)
colorBlack = (0, 0, 0)
colorGreen = (0, 80, 0)
colorBlue = (0, 0, 100)

largeFont = pygame.font.SysFont('Corbel', 100)
font = pygame.font.SysFont('Arial', 40)

#rendering a text written in this font
textGameName = largeFont.render("PyUNO", True, colorBlue)

objects = []

class Button():
    def __init__(self, x, y, width, height, buttonText = 'button', onClickFunction = None, onPress = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onClickFunction = onClickFunction
        self.onePress = onPress
        self.alreadyPressed = False
        self.fillColors = {'nomal' : "#ffffff", 
                           "hover" : "#666666", 
                           "pressed" : "#333333"}
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        #objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['nomal'])
        if self.buttonRect.collidepoint(mousePos): #마우스와 충돌포인트가 충돌 확인
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]: #좌클릭
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onClickFunction()
                elif not self.alreadyPressed:
                    self.onClickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

def singlePlay():
    pass

def showMenu():
    pass

startButton = Button(30, 230, 140, 40, "start", singlePlay)
menuButton = Button(30, 300, 140, 40, "menu", showMenu)
quitButton = Button(30, 370, 140, 40, "quit", pygame.quit)

objects.append(startButton)
objects.append(menuButton)
objects.append(quitButton)

while True:

    screen.fill(colorGreen)
    screen.blit(textGameName, [width // 2 - 100, 70])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for obj in objects:
        obj.process()
    
    pygame.display.flip()