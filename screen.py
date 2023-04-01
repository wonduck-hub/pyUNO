import pygame
import random
import sys
import time
from utils.saveManager import SettingManager
from utils.button import Button
from card import NumberCard, Deck, AbilityCard
from player import HumanPlayer
from player import ComputerPlayer
from player import DiscardPile

class Screen:
    def __init__(self):
        self.setting = SettingManager()
        self.data = self.setting.read()
        self.screen = pygame.display.set_mode(self.data['screenSize'])
        pygame.display.set_caption('PyUNO')
        self.running = True
        

class MapScreen(Screen):
    def __init__(self):
        super().__init__()
        # self.setting = settingManager()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.screen = pygame.display.set_mode(self.data['screenSize'])
      
        self.mapImage = pygame.transform.scale(pygame.image.load("map_image/map.png"), (self.width, self.height))
        self.area1 = pygame.image.load("map_image/area_1.png")
        self.area2 = pygame.image.load("map_image/area_2.png")
        self.area3 = pygame.image.load("map_image/area_3.png")
        self.area4 = pygame.image.load("map_image/area_4.png")
      
        # 이미지 위치
        self.areas = [
              (100, 0),
              (450, 50),
              (100, 200),
              (450, 250)
          ]

        self.mapRect = self.mapImage.get_rect()
        self.area1Rect = self.area1.get_rect(topleft = self.areas[0])
        self.area2Rect = self.area2.get_rect(topleft = self.areas[1])
        self.area3Rect = self.area3.get_rect(topleft = self.areas[2])
        self.area4Rect = self.area4.get_rect(topleft = self.areas[3])
      
        # 각 단계 잠금 상태 초기화
        self.unlockArea1 = True
        self.unlockArea2 = False
        self.unlockArea3 = False
        self.unlockArea4 = False

        self.quitButton = Button(15, 15, 60, 40, "quit", self.screen, self.quit)
    
    def quit(self):
        self.running = False

    def draw(self):
        self.screen.blit(self.mapImage, (0, 0))
      
        for i in range(4):
            self.screen.blit(eval(f"self.area{i+1}"), self.areas[i])

          
    def askStart(self, area):
        # 창 생성
        dialog_x = 350
        dialog_y = 100
        dialog = pygame.Surface((dialog_x, dialog_y))
        dialog.fill((255, 255, 255))
      
        # 텍스트 출력
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Do you want to Battle in Level{area}?", True, (0, 0, 0))
        textRect = text.get_rect(center = (dialog_x // 2, dialog_y // 2))
        dialog.blit(text, textRect)
      
        # 버튼 생성
        acceptButton = pygame.Rect(90, 65, 50, 20)
        refuseButton = pygame.Rect(210, 65, 50, 20)
        pygame.draw.rect(dialog, (255, 0, 0), acceptButton)
        pygame.draw.rect(dialog, (0, 0, 255), refuseButton)
      
        acceptButtonText = font.render("Yes", True, (255, 255, 255))
        acceptButtonTextRect = acceptButtonText.get_rect(center = acceptButton.center)
        dialog.blit(acceptButtonText, acceptButtonTextRect)
      
        refuseButtonText = font.render("No", True, (255, 255, 255))
        refuseButtonTextRect = refuseButtonText.get_rect(center = refuseButton.center)
        dialog.blit(refuseButtonText, refuseButtonTextRect)
      
        dialogRect = dialog.get_rect(center = self.screen.get_rect().center)
        self.screen.blit(dialog, dialogRect)
    
    def run(self):
  
        map = MapScreen()
        map.draw()
        
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                
                # 마우스 클릭으로 지역 선택
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    if self.area1Rect.collidepoint(mousePos):
                        self.askStart(1)
                        
                    elif self.area2Rect.collidepoint(mousePos):    
                        self.askStart(2)
                        
                    elif self.area3Rect.collidepoint(mousePos):
                        self.askStart(3)
                        
                    elif self.area4Rect.collidepoint(mousePos):  
                        self.askStart(4)
            
            self.quitButton.process()
                
        
            pygame.display.flip()
      
      
class StartScreen(Screen):
    def __init__(self):
        super().__init__()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        #나중에 색맹모드 추가시 수정
        self.colorWhite = (255, 255, 255)
        self.colorBlack = (0, 0, 0)
        self.colorBlue = (0, 0, 100)

        self.largeFont = pygame.font.SysFont('Corbel', 100)
        self.font = pygame.font.SysFont('Arial', 35)
        self.smallFont = pygame.font.SysFont('Arial', 15)

        #rendering a text written in this font
        self.textGameName = self.largeFont.render("PyUNO", True, self.colorBlue)
        self.textSelect = self.smallFont.render("[Select!]", True, self.colorBlue)
        self.textHelpEnter = self.font.render("Select : Enter", True, self.colorWhite)
        self.textHelpNextButton = self.font.render("Next : Down or right arrow", True, self.colorWhite)
        self.textHelpBeforButton = self.font.render("Befor : Up or left arrow", True, self.colorWhite)

        #self.settingMenu = SettingScreen()

        self.buttons = []
        self.startButton = Button(30, 210, 140, 40, "single",self.screen)
        self.menuButton = Button(30, 280, 140, 40, "menu", self.screen)
        self.quitButton = Button(30, 350, 140, 40, "quit", self.screen, pygame.quit)
        self.storyButton = Button(190, 210, 140, 40, "story", self.screen)

        self.buttons.append(self.startButton)
        self.buttons.append(self.menuButton)
        self.buttons.append(self.quitButton)
        self.buttons.append(self.storyButton)

    def showSetting(self):
        settingMenu = SettingScreen()
        settingMenu.run()
        self.data = self.setting.read()
        self.screen = pygame.display.set_mode(self.data['screenSize'])
    
    def showInGame(self):
        inGame = LobbyScreen()
        inGame.run()
    
    def showMap(self):
        map = MapScreen()
        map.run()
    
    def run(self):

        self.menuButton.setOnClickFunction(self.showSetting)
        self.startButton.setOnClickFunction(self.showInGame)
        self.storyButton.setOnClickFunction(self.showMap)

        temp = 0
        buttonIndex = 0
        selectPos = self.buttons[0].getPos()
        isShowHelp = False

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT: #화살표 아래, 오른쪽 버튼을 눌렀을 때
                        temp = temp + 1
                        buttonIndex = temp % len(self.buttons)
                        selectPos = self.buttons[buttonIndex].getPos()


                    elif event.key == pygame.K_UP or event.key == pygame.K_LEFT: #화살표 위, 왼쪽 버튼을 눌렀을 떄
                        temp = temp - 1
                        buttonIndex = temp % len(self.buttons)
                        selectPos = self.buttons[buttonIndex].getPos()

                    elif event.key == pygame.K_RETURN:
                        self.buttons[buttonIndex].runFunction()

                    else:
                        startTime = pygame.time.get_ticks()
                        isShowHelp = True
            
            self.screen.fill(self.data['backgroundColor'])
            
            # 여기에 화면에 그리는 코드를 작성합니다.
            for btn in self.buttons:
                btn.process()

            mousePos = pygame.mouse.get_pos()
            self.screen.blit(self.textGameName, [self.width // 2 - 100, 70])
            self.screen.blit(self.textSelect, selectPos)
    
            if isShowHelp:
                self.screen.blit(self.textHelpEnter, 
                                 (self.width // 2 - 50, self.height // 2))
                self.screen.blit(self.textHelpNextButton, 
                                 (self.width // 2 - 50, self.height // 2 + 50))
                self.screen.blit(self.textHelpBeforButton, 
                                 (self.width // 2 - 50, self.height // 2 + 100))

                if pygame.time.get_ticks() - startTime > 1000:
                    isShowHelp = False
                        
            pygame.display.flip()
        
        pygame.quit()


class SettingScreen(Screen):
    def __init__(self):
        super().__init__()
        self.setting = SettingManager()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.font = pygame.font.SysFont('Arial', 35)

        self.textScreenSize = self.font.render("screen size:", True, [255, 255, 255])
        self.textColorBlindness = self.font.render("color blindness:", True, [255, 255, 255])

        self.buttons = []

        self.screenSizeSmallButton = Button(30, 50, 140, 40, "650X400", self.screen, self.smallScreen)
        self.screenSizeMiddleButton = Button(180, 50, 140, 40, "700X450", self.screen, self.middleScreen)
        self.screenSizeLargeButton = Button(330, 50, 140, 40, "750X500", self.screen, self.largeScreen)

        self.screenColorBlindnessOn = Button(30, 145, 140, 40, "on", self.screen)
        self.screenColorBlindnessOff = Button(180, 145, 140, 40, "off", self.screen)

        self.saveButton = Button(self.width - 150, self.height - 100, 140, 40, "save", self.screen, self.saveData)
        self.exitButton = Button(self.width - 150, self.height - 50, 140, 40, "exit", self.screen, self.quitScreen)

        self.resetButton = Button(self.width - 150, 50, 140, 40, "reset", self.screen, self.resetData)
        
        self.keyUpLabel = Button(30,240, 140, 40, "Up", self.screen)
        self.keyDownLabel = Button(30,290, 140, 40, "Down", self.screen)
        self.keyLeftLabel = Button(30,340, 140, 40, "Left", self.screen)
        self.keyRightLabel = Button(30, 390, 140, 40, "Right", self.screen)
        self.keyEnterLabel = Button(330, 240, 140, 40, "Enter", self.screen)

        self.buttons.append(self.screenSizeSmallButton)
        self.buttons.append(self.screenSizeMiddleButton)
        self.buttons.append(self.screenSizeLargeButton)
        self.buttons.append(self.screenColorBlindnessOff)
        self.buttons.append(self.screenColorBlindnessOn)
        self.buttons.append(self.saveButton)
        self.buttons.append(self.exitButton)
        self.buttons.append(self.resetButton)
        self.buttons.append(self.keyUpLabel)
        self.buttons.append(self.keyDownLabel)
        self.buttons.append(self.keyLeftLabel)
        self.buttons.append(self.keyRightLabel)
        self.buttons.append(self.keyEnterLabel)

        self.clicked=False

    def smallScreen(self):
        self.data['screenSize'] = [650, 400]

    def middleScreen(self):
        self.data['screenSize'] = [700, 450]

    def largeScreen(self):
        self.data['screenSize'] = [750, 500]

    def saveData(self):
        self.setting.write(self.data)

    def quitScreen(self):
        self.running = False

    def resetData(self):
        #나중에 추가 필요
        self.data['screenSize'] = [700, 450]
        self.setting.write(self.data)

    def run(self):

        font = pygame.font.Font(None, 32)
    
        keyUpText = font.render( self.data['keyControl'][0], True, (128, 128, 128))
        keyDownText = font.render(self.data['keyControl'][1], True, (128, 128, 128))
        keyLeftText = font.render(self.data['keyControl'][2], True, (128, 128, 128))
        keyRightText = font.render(self.data['keyControl'][3], True, (128, 128, 128))
        keyEnterText = font.render(self.data['keyControl'][4], True, (128, 128, 128))
  
        boxColor = [255, 255, 255]

        self.running = True
        while self.running:
            keyUpBox = pygame.Rect(180,240, 140, 40)
            keyDownBox = pygame.Rect(180,290, 140, 40)
            keyLeftBox = pygame.Rect(180,340, 140, 40)
            keyRightBox = pygame.Rect(180,390, 140, 40)
            keyEnterBox = pygame.Rect(480,240, 140, 40)

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if keyUpBox.collidepoint(event.pos):
                        keyUpText = font.render("", True, (128, 128, 128))
                        number=0
                        self.clicked=True
                    if keyDownBox.collidepoint(event.pos):
                        keyDownText = font.render("", True, (128, 128, 128))
                        number=1
                        self.clicked=True
                    if keyLeftBox.collidepoint(event.pos):
                        keyLeftText = font.render("", True, (128, 128, 128))
                        number=2
                        self.clicked=True
                    if keyRightBox.collidepoint(event.pos):
                        keyRightText = font.render("", True, (128, 128, 128))
                        number=3
                        self.clicked=True
                    if keyEnterBox.collidepoint(event.pos):
                        keyEnterText = font.render("", True, (128, 128, 128))
                        number=4
                        self.clicked=True
                if event.type == pygame.KEYDOWN and self.clicked:
                        newKey = pygame.key.name(event.key)
                        self.data['keyControl'][number] =  newKey
                        self.setting.write(self.data)
                        if number==0:
                            keyUpText = font.render(newKey, True, (128, 128, 128))
                            self.clicked=False
                        elif number==1:
                            keyDownText = font.render(newKey, True, (128, 128, 128))
                            self.clicked=False
                        elif number==2:
                            keyLeftText = font.render(newKey, True, (128, 128, 128))
                            self.clicked=False
                        elif number==3:
                            keyRightText = font.render(newKey, True, (128, 128, 128))
                            self.clicked=False
                        elif number==4:
                            keyEnterText = font.render(newKey, True, (128, 128, 128))
                            self.clicked=False
                    

            self.screen.fill(self.data['backgroundColor'])

            self.screen.blit(self.textScreenSize, [30, 5])
            self.screen.blit(self.textColorBlindness, [30, 100])

            for btn in self.buttons:
                btn.process()
            
            pygame.draw.rect(self.screen, boxColor, keyUpBox)
            pygame.draw.rect(self.screen, boxColor, keyDownBox)
            pygame.draw.rect(self.screen, boxColor, keyLeftBox)
            pygame.draw.rect(self.screen, boxColor, keyRightBox)
            pygame.draw.rect(self.screen, boxColor, keyEnterBox)

            self.screen.blit(keyUpText, (180,240))
            self.screen.blit(keyDownText, (180,290))
            self.screen.blit(keyLeftText, (180,340))
            self.screen.blit(keyRightText, (180,390))
            self.screen.blit(keyEnterText, (480,240))

            pygame.display.flip()
        
class LobbyScreen(Screen):
    def __init__(self):
        super().__init__()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.nameText = 'player'
        self.computerNum = 1
        self.font = pygame.font.SysFont('Arial', 35)

        self.textName = self.font.render('name', True, (255, 255, 255))
        self.textNumberOfComputer = self.font.render('NumberOfComputer', True, (255, 255, 255))

        self.inputBox = pygame.Rect(50, 60, 140, 32)

        self.buttons = []

        self.exitButton = Button(150, self.data['screenSize'][1] // 2 + 60, 140, 40, "quit", self.screen, self.quitScreen)
        self.saveButton = Button(150, self.data['screenSize'][1] // 2, 140, 40, "start", self.screen, self.startGame)

        self.buttons.append(self.exitButton)
        self.buttons.append(self.saveButton)
    
    def startGame(self):
        computerList = []
        for i in range(0, self.computerNum):
            computerList.append(ComputerPlayer('computer' + str(i + 1)))
        SingleGameScreen(self.nameText, computerList).run()
        self.data = self.setting.read()
        self.running = False

    def quitScreen(self):
        self.running = False

    def run(self):
        font = pygame.font.Font(None, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        done = False
        listColor = [30, 30, 30]

        font = pygame.font.SysFont('Arial', 20)

        computer1Text = font.render('computer1', True, (128, 128, 128))
        computer2Text = font.render('add to click', True, (128, 128, 128))
        computer3Text = font.render('add to click', True, (128, 128, 128))
        computer4Text = font.render('add to click', True, (128, 128, 128))
        computer5Text = font.render('add to click', True, (128, 128, 128))


        computer2Color = [255, 255, 255]
        computer3Color = [255, 255, 255]
        computer4Color = [255, 255, 255]
        computer5Color = [255, 255, 255]
    
        self.running = True
        while self.running:
            computer1 = pygame.Rect([(self.data['screenSize'][0] // 4) * 3 + 2, 0 + 2], [self.data['screenSize'][0] - 2, self.data['screenSize'][1] // 5 - 2])
            computer2 = pygame.Rect([(self.data['screenSize'][0] // 4) * 3 + 2, (self.data['screenSize'][1] // 5) + 2], [self.data['screenSize'][0] - 2, (self.data['screenSize'][1] // 5) - 2])
            computer3 = pygame.Rect([(self.data['screenSize'][0] // 4) * 3 + 2, (self.data['screenSize'][1] // 5) * 2 + 2], [self.data['screenSize'][0] - 2, (self.data['screenSize'][1] // 5) - 2])
            computer4 = pygame.Rect([(self.data['screenSize'][0] // 4) * 3 + 2, (self.data['screenSize'][1] // 5) * 3 + 2], [self.data['screenSize'][0] - 2, (self.data['screenSize'][1] // 5) - 2])
            computer5 = pygame.Rect([(self.data['screenSize'][0] // 4) * 3 + 2, (self.data['screenSize'][1] // 5) * 4 + 2], [self.data['screenSize'][0] - 2, (self.data['screenSize'][1] // 5) - 2])
            #self.data = self.setting.read()
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if self.inputBox.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    if computer2.collidepoint(event.pos):
                        if computer2Color == [255, 255, 255]:
                            computer2Color = [50, 50, 50]
                            computer2Text = font.render('computer2', True, (128, 128, 128))
                            self.computerNum = self.computerNum + 1
                        else:
                            computer2Color = [255, 255, 255]
                            computer2Text = font.render('add to click', True, (128, 128, 128))
                            self.computerNum = self.computerNum - 1
                    if computer3.collidepoint(event.pos):
                        if computer3Color == [255, 255, 255]:
                            computer3Color = [50, 50, 50]
                            computer3Text = font.render('computer3', True, (128, 128, 128))
                            self.computerNum = self.computerNum + 1
                        else:
                            computer3Color = [255, 255, 255]
                            computer3Text = font.render('add to click', True, (128, 128, 128))
                            self.computerNum = self.computerNum - 1
                    if computer4.collidepoint(event.pos):
                        if computer4Color == [255, 255, 255]:
                            computer4Color = [50, 50, 50]
                            computer4Text = font.render('computer4', True, (128, 128, 128))
                            self.computerNum = self.computerNum + 1
                        else:
                            computer4Color = [255, 255, 255]
                            computer4Text = font.render('add to click', True, (128, 128, 128))
                            self.computerNum = self.computerNum - 1
                    if computer5.collidepoint(event.pos):
                        if computer5Color == [255, 255, 255]:
                            computer5Color = [50, 50, 50]
                            computer5Text = font.render('computer5', True, (128, 128, 128))
                            self.computerNum = self.computerNum + 1
                        else:
                            computer5Color = [255, 255, 255]
                            computer5Text = font.render('add to click', True, (128, 128, 128))
                            self.computerNum = self.computerNum - 1
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            self.nameText = self.nameText[:-1]
                        else:
                            self.nameText += event.unicode

            # TODO 텍스트 박스에 텍스티 입력 추가
            self.screen.fill(self.data['backgroundColor'])

            pygame.draw.rect(self.screen, listColor, [(self.data['screenSize'][0] // 4) * 3, 0, (self.data['screenSize'][0]), self.data['screenSize'][1]])

            self.screen.blit(self.textName, [50, 5])
            pygame.draw.rect(self.screen, [50, 50, 50], computer1)
            pygame.draw.rect(self.screen, computer2Color, computer2)
            pygame.draw.rect(self.screen, computer3Color, computer3)
            pygame.draw.rect(self.screen, computer4Color, computer4)
            pygame.draw.rect(self.screen, computer5Color, computer5)

            self.screen.blit(computer1Text, [(self.data['screenSize'][0] // 4) * 3 + 50, 2])
            self.screen.blit(computer2Text, [(self.data['screenSize'][0] // 4) * 3 + 50, (self.data['screenSize'][1] // 5)])
            self.screen.blit(computer3Text, [(self.data['screenSize'][0] // 4) * 3 + 50, (self.data['screenSize'][1] // 5) * 2])
            self.screen.blit(computer4Text, [(self.data['screenSize'][0] // 4) * 3 + 50, (self.data['screenSize'][1] // 5) * 3])
            self.screen.blit(computer5Text, [(self.data['screenSize'][0] // 4) * 3 + 50, (self.data['screenSize'][1] // 5) * 4])

            txt_surface = font.render(self.nameText, True, color)
            width = max(200, txt_surface.get_width()+10)
            self.inputBox.w = width
            # Blit the text.
            self.screen.blit(txt_surface, (self.inputBox.x+5, self.inputBox.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(self.screen, color, self.inputBox, 2)

            for btn in self.buttons:
                btn.process()

            pygame.display.flip()

class SingleGameScreen(Screen):
    
    def __init__(self, name, computerList):
        super().__init__()
        self.playerName = name
        self.player = HumanPlayer(name)
        self.computerList  = []
        self.computerList = self.computerList + computerList
        self.deck = Deck(self.screen)
        self.discard = DiscardPile()
        self.nowTurnPlayer = None
        self.index = random.randrange(0, 4)
        self.turnNum = 1
        self.comTurnTime = 0
        self.humanStartTime = 0
        self.nowTurnList = []
        self.runChangeColor = True
        self.changeColor = 'None'
        self.haveWiner = False

        self.setting = SettingManager()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()


        self.escButtons = []

        self.quitButton= Button(20, (self.height // 4), 160, 40, 'quit game', self.screen, self.quitScreen)
        self.settingButton = Button(20, (self.height // 4) * 2, 100, 40, 'setting', self.screen, self.showSetting)

        self.escButtons.append(self.quitButton)
        self.escButtons.append(self.settingButton)
        
        self.buttons = []

        self.unoButton = Button(10, self.data['screenSize'][1] - 50, 100, 35, 'UNO', self.screen, self.uno)
        self.drawCardButton = Button(self.data['screenSize'][0] // 4 - 80, self.data['screenSize'][1] // 3,60, 35, 'add', self.screen, self.drawCard)

    def endTurn(self):
        self.index = self.index + self.turnNum
        self.nowTurnPlayer = self.nowTurnList[self.index % len(self.nowTurnList)]
        self.comTurnTime = pygame.time.get_ticks() + self.nowTurnPlayer.time
        self.humanStartTime = pygame.time.get_ticks()

    def drawCard(self):
        self.nowTurnPlayer.addCard(self.deck.drawCard())
        self.endTurn()
            

    def quitScreen(self):
        self.running = False

    def ability(self, ability):
        if self.discard.cards[0].value == 'draw2':
            self.endTurn()
            self.nowTurnPlayer.addCard(self.deck.drawCard())
            self.nowTurnPlayer.addCard(self.deck.drawCard())
        elif self.discard.cards[0].value == 'oneMore':
            self.index = self.index - self.turnNum
            self.endTurn()
        elif self.discard.cards[0].value == 'reverse':
            self.turnNum = self.turnNum * -1
            self.endTurn()
        elif self.discard.cards[0].value == 'skip':
            self.index = self.index + self.turnNum
            self.endTurn()
        elif self.discard.cards[0].value == 'joker':
            self.endTurn()
            self.nowTurnPlayer.addCard(self.deck.drawCard())
            self.nowTurnPlayer.addCard(self.deck.drawCard())
            self.nowTurnPlayer.addCard(self.deck.drawCard())
            self.nowTurnPlayer.addCard(self.deck.drawCard())
            self.nowTurnPlayer.addCard(self.deck.drawCard())
        elif self.discard.cards[0].value == 'defense':
            #TODO 승리 카드
            pass
        elif self.discard.cards[0].value == 'changeColor':
            screen = pygame.display.set_mode(self.data['screenSize'])
            self.runChangeColor = True
            red = Button(self.data['screenSize'][0] // 5 - 50, self.data['screenSize'][1] // 2, 100, 35, 'red', self.screen, self.red)
            blue = Button(self.data['screenSize'][0] // 5 * 2 - 50, self.data['screenSize'][1] // 2, 100, 35, 'blue', self.screen, self.blue)
            green = Button(self.data['screenSize'][0] // 5 * 3 - 50, self.data['screenSize'][1] // 2, 100, 35, 'green', self.screen, self.green)
            yellow = Button(self.data['screenSize'][0] // 5 * 4 - 50, self.data['screenSize'][1] // 2, 100, 35, 'yellow', self.screen, self.yellow)
            while self.runChangeColor:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        self.running = False
                
                self.screen.fill([255, 255, 255])
                red.process()
                blue.process()
                green.process()
                yellow.process()
                pygame.display.flip()
            self.endTurn()

        else:
            self.endTurn()
            print('기술 안나감')
    
    def red(self):
        self.runChangeColor = False
        self.changeColor = 'red'

    def blue(self):
        self.runChangeColor = False
        self.changeColor = 'blue'

    def green(self):
        self.runChangeColor = False
        self.changeColor = 'green'

    def yellow(self):
        self.runChangeColor = False
        self.changeColor = 'yellow'

    def showSetting(self):
        settingMenu = SettingScreen()
        settingMenu.run()
        self.data = self.setting.read()
        self.screen = pygame.display.set_mode(self.data['screenSize'])
        self.unoButton = Button(10, self.data['screenSize'][1] - 50, 100, 35, 'UNO', self.screen)
        self.drawCardButton = Button(self.data['screenSize'][0] // 4 - 80, self.data['screenSize'][1] // 3,60, 35, 'add', self.screen, self.drawCard)

    def uno(self):
        if isinstance(self.nowTurnPlayer, HumanPlayer):
            if len(self.nowTurnPlayer.handsOnCard) == 2:
                self.nowTurnPlayer.checkUno = True
            else:
                self.nowTurnPlayer.addCard(self.deck.drawCard())
        elif isinstance(self.nowTurnPlayer, ComputerPlayer):
            pass

    def run(self):

        handsOnColor = [0, 120, 0]
        listColor = [30, 30, 30]
        isInputEsc = False

        #게임 시작시 실행되는 내용
        font = pygame.font.SysFont('Arial', 25)
        winFont = pygame.font.SysFont('Arial', 60)
        self.deck.createDeck()
        self.player.handsOnCard = self.player.handsOnCard + [AbilityCard('None', 'joker', self.screen)] #self.deck.prepareCard()
        self.deck.shuffle()
        self.nowTurnList = self.computerList + [self.player]
        self.discard.addCard(self.deck.drawCard())
        if isinstance(self.discard.cards[0], AbilityCard):
            self.ability(self.discard.cards[0])

        self.nowTurnPlayer = self.nowTurnList[self.index % len(self.nowTurnList)]
        self.comTurnTime = pygame.time.get_ticks() + self.nowTurnPlayer.time
        self.humanStartTime = pygame.time.get_ticks()

        clock = pygame.time.Clock()

        for i in range(len(self.computerList)):#카드 분배
            self.computerList[i].handsOnCard = self.computerList[i].handsOnCard + self.deck.prepareCard()


        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and isinstance(self.nowTurnPlayer, HumanPlayer):
                    for i in range(len(self.nowTurnPlayer.handsOnCard)):
                        if self.nowTurnPlayer.handsOnCard[i].canInsert and self.nowTurnPlayer.handsOnCard[i].isClicked(pygame.mouse.get_pos()):
                            self.nowTurnPlayer.pushCard(i, self.discard)
                            if isinstance(self.discard.cards[0], AbilityCard):
                                if self.nowTurnPlayer.checkUno == False and len(self.nowTurnPlayer.handsOnCard) == 1:
                                    self.nowTurnPlayer.addCard(self.deck.drawCard())
                                self.ability(self.discard.cards[0].value)
                            else:
                                if self.nowTurnPlayer.checkUno == False and len(self.nowTurnPlayer.handsOnCard) == 1:
                                    self.nowTurnPlayer.addCard(self.deck.drawCard())
                                self.endTurn()
                            self.nowTurnPlayer.checkUno = False
                            break
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if isInputEsc:
                            isInputEsc = False
                        else:
                            isInputEsc = True

            if self.haveWiner:
                text = ''
                quitButton = Button(self.data['screenSize'][0] // 2 - 50, self.data['screenSize'][1] // 3 * 2, 100, 35, 'quit', self.screen, self.quitScreen)
                self.screen.fill([255, 255, 255])
                for p in self.nowTurnList:
                    if len(p.handsOnCard) == 0:
                        text = p.name
                winText = winFont.render('winder : ' + text, True, (0, 0, 0))
                self.screen.blit(winText, (self.data['screenSize'][0] // 2 - 150, self.data['screenSize'][1] // 3))
                quitButton.process()
                pygame.display.flip()

            if isInputEsc:
                self.screen.fill([255, 255, 255])

                for btn in self.escButtons:
                    btn.process()

                pygame.display.flip()
                #TODO 이 상태에선 타이머는 멈춰 있어야 함

            else:
                #현제 턴 표시
                self.nowTurnPlayer = self.nowTurnList[self.index % len(self.nowTurnList)]
                nowTurnText = font.render('now turn : ' + self.nowTurnPlayer.name , True, (255, 255, 255))
                nextTurnText = font.render('next turn : ' + self.nowTurnList[(self.index + self.turnNum) % len(self.nowTurnList)].name, True, (255, 255, 255))

                self.screen.fill(self.data['backgroundColor'])
                self.screen.blit(nowTurnText, (self.data['screenSize'][0] // 2 - 100, 2))
                self.screen.blit(nextTurnText, (self.data['screenSize'][0] // 2 - 100, 30))

                # 영역 별 컬러
                pygame.draw.rect(self.screen, handsOnColor, [0, (self.data['screenSize'][1] // 3) * 2, self.data['screenSize'][0], self.data['screenSize'][1]])
                pygame.draw.rect(self.screen, listColor, [(self.data['screenSize'][0] // 4) * 3, 0, self.data['screenSize'][0], self.data['screenSize'][1]])
                #카드들 출력
                self.player.showHandsOnCard(50, self.data['screenSize'][1] // 10 * 7)

                self.deck.show(self.data['screenSize'][0] // 4, self.data['screenSize'][1] // 3)

                self.discard.show(self.data['screenSize'][0] // 4 * 2 - 50, self.data['screenSize'][1] // 3, self.changeColor, self.screen)

                #컴퓨터 카드 출력
                for i in range(len(self.computerList)):
                    self.computerList[i].showHandsOnCard(self.data['screenSize'][0] // 4 * 3 + 50, self.data['screenSize'][1] // 5 * i, self.screen)

                #버튼 출력
                self.unoButton.process()
                
                for p in self.nowTurnList:
                    if len(p.handsOnCard) == 0:
                        self.haveWiner = True

                #컴퓨터의 턴
                if isinstance(self.nowTurnPlayer, ComputerPlayer):
                    if pygame.time.get_ticks() - self.comTurnTime > 800:
                        if self.nowTurnPlayer.playTurn(self.discard, self.changeColor):
                            if isinstance(self.discard.cards[0], AbilityCard):
                                self.ability(self.discard.cards[0].value)
                            else:
                                self.endTurn()
                        else:
                            self.drawCard()

                elif isinstance(self.nowTurnPlayer, HumanPlayer):#플레이어의 턴
                    #내 턴 일때 출력
                    self.nowTurnPlayer.checkCandInsert(self.discard, self.changeColor)
                    elapsedTime = (pygame.time.get_ticks() - self.humanStartTime) / 1000
                    timer = font.render('time : ' + str(int(self.nowTurnPlayer.totalTime - elapsedTime)), True, (255, 255, 255))
                    self.screen.blit(timer,(10, 10))

                    if self.nowTurnPlayer.totalTime - elapsedTime <= 0:#타임 오버
                        self.drawCard()

                    self.drawCardButton.process()

                pygame.display.flip()
                    



if __name__ == '__main__':
    pygame.init()
    setting = SingleGameScreen('player', [ComputerPlayer('computer1'), ComputerPlayer('computer2'), ComputerPlayer('computer3')])
    setting.run()
