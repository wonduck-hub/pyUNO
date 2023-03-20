import pygame
from settings import *
from utils.button import Button
import os

def menu():
   screenSizes = [[600 , 400], [700, 450], [800, 500]]
   screen = pygame.display.set_mode(size)

   buttons = []

   screenSizeSmall = Button(30, 230, 140, 40, "small screen", screen)

   while True:
      screen.fill(backgroundColor)
      mousePos = pygame.mouse.get_pos()



      pygame.display.flip()