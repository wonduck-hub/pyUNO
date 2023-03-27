import pygame
from utils.saveManager import settingManager
from utils.button import Button
from card import NumberCard
from player import HumanPlayer

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
        
        self.buttons.append(self.screenSizeSmallButton)
        self.buttons.append(self.screenSizeMiddleButton)
        self.buttons.append(self.screenSizeLargeButton)
        self.buttons.append(self.screenColorBlindnessOff)
        self.buttons.append(self.screenColorBlindnessOn)
        self.buttons.append(self.saveButton)
        self.buttons.append(self.exitButton)
        self.buttons.append(self.resetButton)

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
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False

            self.screen.fill(self.data['backgroundColor'])

            self.screen.blit(self.textScreenSize, [30, 5])
            self.screen.blit(self.textColorBlindness, [30, 100])

            for btn in self.buttons:
                btn.process()

            pygame.display.flip()
        
class LobbyScreen(Screen):
    def __init__(self):
        super().__init__()
        self.setting = settingManager()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.nameText = ''
        self.computerNum = 1
        self.font = pygame.font.SysFont('Arial', 35)

        self.textName = self.font.render('name', True, (255, 255, 255))
        self.textNumberOfComputer = self.font.render('NumberOfComputer', True, (255, 255, 255))

        self.inputBox = pygame.Rect(50, 60, 140, 32)

        self.buttons = []

        self.exitButton = Button(self.width - 150, self.height - 50, 140, 40, "exit", self.screen, self.quitScreen)
        self.saveButton = Button(self.width - 150, self.height - 100, 140, 40, "start", self.screen, self.startGame)

        self.oneButton = Button(50, self.height // 2 + 60, 40, 40, "1", self.screen, self.one)
        self.twoButton = Button(100, self.height // 2 + 60, 40, 40, "2", self.screen, self.two)
        self.threeButton = Button(150, self.height // 2 + 60, 40, 40, "3", self.screen, self.three)
        self.fourButton = Button(200, self.height // 2 + 60, 40, 40, "4", self.screen, self.four)
        self.fiveButton = Button(250, self.height // 2 + 60, 40, 40, "5", self.screen, self.five)

        self.buttons.append(self.exitButton)
        self.buttons.append(self.saveButton)
        self.buttons.append(self.oneButton)
        self.buttons.append(self.twoButton)
        self.buttons.append(self.threeButton)
        self.buttons.append(self.fourButton)
        self.buttons.append(self.fiveButton)
    
    def one(self):
        self.computerNum = 1

    def two(self):
        self.computerNum = 2

    def three(self):
        self.computerNum = 3

    def four(self):
        self.computerNum = 4

    def five(self):
        self.computerNum = 5

    def startGame(self):
        SingleGameScreen(self.nameText, self.computerNum).run()

    def quitScreen(self):
        self.running = False

    def run(self):
        font = pygame.font.Font(None, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        done = False
    
        self.running = True
        while self.running:
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
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            print(self.nameText)
                            self.nameText = ''
                        elif event.key == pygame.K_BACKSPACE:
                            self.nameText = self.nameText[:-1]
                        else:
                            self.nameText += event.unicode

            # TODO 텍스트 박스에 텍스티 입력 추가
            self.screen.fill(self.data['backgroundColor'])

            self.screen.blit(self.textName, [50, 5])
            self.screen.blit(self.textNumberOfComputer, [50, self.height // 2])

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
    
    def __init__(self, name, computerNum):
        super().__init__()
        self.playerName = name
        self.computerNum = computerNum
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
                pygame.draw.rect(self.screen, handsOnColor, [0, (self.height // 3) * 2, self.width, self.height])
                pygame.draw.rect(self.screen, listColor, [(self.width // 4) * 3, 0, self.width, self.height])

                testCard.show(self.width // 2, self.height // 2)

                # 버튼 출력
                for btn in self.buttons:
                    btn.process()

            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    setting = LobbyScreen()
    setting.run()