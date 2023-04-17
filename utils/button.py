import pygame
from utils.sound import SoundManager
from utils.sound import sound

class Button():
    def __init__(self, x, y, width, height, buttonText = 'button', 
                 screen = None, onClickFunction = None, onPress = False):
        #self.sound = SoundManager()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.__onClickFunction = onClickFunction
        self.__onePress = onPress
        self.__alreadyPressed = False
        self.__fillColors = {'nomal' : "#cccccc", 
                           "hover" : "#666666", 
                           "pressed" : "#333333"}
        self.__buttonSurface = pygame.Surface((self.width, self.height))
        self.__buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.__font = pygame.font.SysFont('Arial', 35)
        self.__buttonSurf = self.__font.render(buttonText, True, (20, 20, 20))
        self.__screen = screen

    def runFunction(self):
        sound.playClickSound()
        if self.__onClickFunction != None:
            self.__onClickFunction()

    def getPos(self):
        return (self.x, self.y)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def setOnClickFunction(self, onClickFunction):
        self.__onClickFunction = onClickFunction

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.__buttonSurface.fill(self.__fillColors['nomal'])
        if self.__buttonRect.collidepoint(mousePos): #마우스와 충돌포인트가 충돌 확인
            self.__buttonSurface.fill(self.__fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]: #좌클릭
                self.__buttonSurface.fill(self.__fillColors['pressed'])
                if self.__onePress:
                    self.runFunction()
                elif not self.__alreadyPressed:
                    self.runFunction()
                    self.__alreadyPressed = True
            else:
                self.__alreadyPressed = False
        self.__buttonSurface.blit(self.__buttonSurf, [
            self.__buttonRect.width/2 - self.__buttonSurf.get_rect().width/2,
            self.__buttonRect.height/2 - self.__buttonSurf.get_rect().height/2
        ])
        self.__screen.blit(self.__buttonSurface, self.__buttonRect)