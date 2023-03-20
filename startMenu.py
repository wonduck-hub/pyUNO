import pygame
from utils.button import Button
#from .settingMenu import menu
import sys

#from settingMenu import screenSizes

pygame.init()

size = [700, 450]
screen = pygame.display.set_mode(size)

title = "pyUNO"
pygame.display.set_caption(title)

width = screen.get_width()
height = screen.get_height()

colorWhite = (255, 255, 255)
colorBlack = (0, 0, 0)
backgroundColor = (0, 80, 0)
colorBlue = (0, 0, 100)

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

def menu():
    pass
def singlePlay():
    pass

startButton = Button(30, 230, 140, 40, "start", screen, singlePlay)
menuButton = Button(30, 300, 140, 40, "menu", screen, menu)
quitButton = Button(30, 370, 140, 40, "quit", screen, pygame.quit)

buttons.append(startButton)
buttons.append(menuButton)
buttons.append(quitButton)

temp = 0
buttonIndex = 0
selectPos = buttons[0].getPos()
isShowHelp = False

while True:

    mousePos = pygame.mouse.get_pos()

    screen.fill(backgroundColor)
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

    if isShowHelp:
        screen.blit(textHelpEnter, (width // 2 - 50, height // 2))
        screen.blit(textHelpNextButton, (width // 2 - 50, height // 2 + 50))
        screen.blit(textHelpBeforButton, (width // 2 - 50, height // 2 + 100))

        if pygame.time.get_ticks() - startTime > 1000:
            isShowHelp = False

    pygame.display.flip()
