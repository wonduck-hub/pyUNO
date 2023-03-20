import pygame
from utils.saveManager import settingManager
from utils.button import Button
#TODO setting menu 화면 크기 적용
setting = settingManager()
data = setting.read()

def smallSize():
   data['screenSize'] = [650, 400]

def middleSize():
   data['screenSize'] = [700, 450]

def largeSize():
   data['screenSize'] = [750, 500]

def saveData():
   setting.write(data)

def menu():
   screen = pygame.display.set_mode([700, 450])
   
   font = pygame.font.SysFont('Arial', 35)

   textScreenSize = font.render("screen size:", True, [255, 255, 255])
   textColorBlindness = font.render("color blindness:", True, [255, 255, 255])

   buttons = []

   screenSizeSmallButton = Button(30, 50, 140, 40, "650X400", screen, smallSize)
   screenSizeMiddleButton = Button(180, 50, 140, 40, "700X450", screen, middleSize)
   screenSizeLargeButton = Button(330, 50, 140, 40, "750X500", screen, largeSize)

   screenColorBlindnessOn = Button(30, 145, 140, 40, "on", screen)
   screenColorBlindnessOff = Button(180, 145, 140, 40, "off", screen)

   saveButton = Button(500, 400, 140, 40, "save", screen, saveData)
   exitButton = Button(350, 400, 140, 40, "exit", screen)

   buttons.append(screenSizeSmallButton)
   buttons.append(screenSizeMiddleButton)
   buttons.append(screenSizeLargeButton)
   buttons.append(screenColorBlindnessOff)
   buttons.append(screenColorBlindnessOn)
   buttons.append(saveButton)
   buttons.append(exitButton)

   while True:
      screen.fill([0, 80, 0])
      mousePos = pygame.mouse.get_pos()

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
         elif event.type == pygame.MOUSEBUTTONDOWN and(mousePos[0] >350 and mousePos[0] < 490) and (mousePos[1] > 400 and mousePos[1] < 440):
            data = setting.read()
            screen = pygame.display.set_mode(data['screenSize'])
            return
         
      screen.blit(textScreenSize, [30, 5])
      screen.blit(textColorBlindness, [30, 100])
      
      for btn in buttons:
         btn.process()

      pygame.display.flip()
