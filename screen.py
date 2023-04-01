import pygame
import sys
from utils.saveManager import settingManager
from utils.button import Button
from card import NumberCard
from player import HumanPlayer
from player import ComputerPlayer

class Screen:
    def __init__(self):
        self.setting = settingManager()
        self.data = self.setting.read()
        self.screen = pygame.display.set_mode(self.data['screenSize'])
        pygame.display.set_caption('PyUNO')
        self.running = True

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

        self.buttons.append(self.startButton)
        self.buttons.append(self.menuButton)
        self.buttons.append(self.quitButton)

    def showSetting(self):
        settingMenu = SettingScreen()
        settingMenu.run()
        self.data = self.setting.read()
        self.screen = pygame.display.set_mode(self.data['screenSize'])
    
    def showInGame(self):
        inGame = LobbyScreen()
        inGame.run()
    
    def run(self):

        self.menuButton.setOnClickFunction(self.showSetting)
        self.startButton.setOnClickFunction(self.showInGame)

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
        self.setting = settingManager()
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
        self.computerList = computerList
        self.setting = settingManager()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.escButtons = []

        self.quitButton= Button(20, (self.height // 4), 160, 40, 'quit game', self.screen, self.quitScreen)
        self.settingButton = Button(20, (self.height // 4) * 2, 100, 40, 'setting', self.screen, self.showSetting)

        self.escButtons.append(self.quitButton)
        self.escButtons.append(self.settingButton)
        

        self.buttons = []

        self.unoButton = Button(10, self.height - 50, 100, 35, 'UNO', self.screen)

        self.buttons.append(self.unoButton)

    def quitScreen(self):
        self.running = False

    def showSetting(self):
        settingMenu = SettingScreen()
        settingMenu.run()
        self.data = self.setting.read()
        self.screen = pygame.display.set_mode(self.data['screenSize'])

    def run(self):

        handsOnColor = [0, 120, 0]
        listColor = [30, 30, 30]
        isInputEsc = False

        me = HumanPlayer(self.playerName)

        testCard = NumberCard('red', '1', self.screen)

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if isInputEsc:
                            isInputEsc = False
                        else:
                            isInputEsc = True
                
            
            if isInputEsc:
                self.screen.fill([255, 255, 255])

                for btn in self.escButtons:
                    btn.process()

                #TODO 이 상태에선 타이머는 멈춰 있어야 함

            else:
                self.screen.fill(self.data['backgroundColor'])

                # 영역 별 컬러
                pygame.draw.rect(self.screen, handsOnColor, [0, (self.data['screenSize'][1] // 3) * 2, self.data['screenSize'][0], self.data['screenSize'][1]])
                pygame.draw.rect(self.screen, listColor, [(self.data['screenSize'][0] // 4) * 3, 0, self.data['screenSize'][0], self.data['screenSize'][1]])

                testCard.show(self.width // 2, self.height // 2)

                # 버튼 출력
                for btn in self.buttons:
                    btn.process()

            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    setting = LobbyScreen()
    setting.run()
