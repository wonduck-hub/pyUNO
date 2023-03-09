import pygame
import sys

import Button

pygame.init()

size = [1600, 900]
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

#rendering a text written in this font
textGameName = largeFont.render("PyUNO", True, colorBlue)

objects = []

def singlePlay():
    pass

def showMenu():
    pass

startButton = Button(30, 230, 140, 40, "start", singlePlay)
menuButton = Button(30, 300, 140, 40, "menu", showMenu)
quitButton = Button(30, 370, 140, 40, "quit", pygame.quit)

run = True
while run:

    screen.fill(colorGreen)
    screen.blit(textGameName, [width // 2 - 100, 70])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for obj in objects:
        obj.process()
    
    pygame.display.flip()