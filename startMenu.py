import pygame
import sys

pygame.init()

size = [700, 450]
screen = pygame.display.set_mode(size)

title = "pyUNO"
pygame.display.set_caption(title)

width = screen.get_width()
height = screen.get_height()

#color
colorWhite = (255, 255, 255)
colorBlack = (0, 0, 0)
colorGreen = (0, 80, 0)
colorBlue = (0, 0, 100)

#font
largeFont = pygame.font.SysFont('Corbel', 100)
font = pygame.font.SysFont('Arial', 40)
smallFont = pygame.font.SysFont('Arial', 15)

#rendering a text written in this font
textGameName = largeFont.render("PyUNO", True, colorBlue)
textSelect = smallFont.render("[Enter!]", True, colorBlue)
textHelpEnter = font.render("Select : Enter", True, colorWhite)
textHelpNextButton = font.render("Next : Down or right arrow", True, colorWhite)
textHelpBeforButton = font.render("Befor : Up or left arrow", True, colorWhite)

buttons = []

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
        self.selected = False

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
        screen.blit(self.buttonSurface, self.buttonRect)

def singlePlay():
    pass

def showMenu():
    pass

startButton = Button(30, 230, 140, 40, "start", singlePlay)
menuButton = Button(30, 300, 140, 40, "menu", showMenu)
quitButton = Button(30, 370, 140, 40, "quit", pygame.quit)

buttons.append(startButton)
buttons.append(menuButton)
buttons.append(quitButton)

#현제 버튼 인덱스를 구하기 위한 것
temp = 0
buttonIndex = 0

#선택된 버튼 표시용
selectPos = buttons[0].getPos()

#설면문 출력 여부
isShowHelp = False

while True:

    mousePos = pygame.mouse.get_pos()

    screen.fill(colorGreen)
    screen.blit(textGameName, [width // 2 - 100, 70])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT: #화살표 아래, 오른쪽 버튼을 눌렀을 때
                temp = temp + 1
                buttonIndex = temp % len(buttons)
                selectPos = buttons[buttonIndex].getPos()


            elif event.key == pygame.K_UP or event.key == pygame.K_LEFT: #화살표 위, 왼쪽 버튼을 눌렀을 떄
                temp = temp - 1
                buttonIndex = temp % len(buttons)
                selectPos = buttons[buttonIndex].getPos()

            elif event.key == pygame.K_RETURN:
                buttons[buttonIndex].onClickFunction()

            else:
                startTime = pygame.time.get_ticks()
                isShowHelp = True

    for btn in buttons:
        btn.process()
    
    screen.blit(textSelect, selectPos)

    if isShowHelp: #키 설명 출력
        screen.blit(textHelpEnter, (width // 2 - 50, height // 2))
        screen.blit(textHelpNextButton, (width // 2 - 50, height // 2 + 50))
        screen.blit(textHelpBeforButton, (width // 2 - 50, height // 2 + 100))

        if pygame.time.get_ticks() - startTime > 1000:
            isShowHelp = False

    pygame.display.flip()
