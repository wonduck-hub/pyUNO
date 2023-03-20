import pygame

class Button():
    def __init__(self, x, y, width, height, buttonText = 'button', screen = None, onClickFunction = None, onPress = False):
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
        font = pygame.font.SysFont('Arial', 40)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        self.selected = False
        self.screen = screen

    def getPos(self):
        return (self.x, self.y)

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
        self.screen.blit(self.buttonSurface, self.buttonRect)