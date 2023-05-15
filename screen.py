import pygame
import random
import socket
import sys
import time
import datetime
from utils.saveManager import SaveManager
from utils.saveManager import save
from utils.button import Button
from utils.socket import Server, Client
from utils.sound import sound
from card import NumberCard, Deck, AbilityCard
from player import HumanPlayer
from player import ComputerPlayer
from player import DiscardPile
from player import ComputerPlayerA

hostName = socket.gethostname()
ip = socket.gethostbyname(hostName)
server = Server(ip)
client = Client()

class Screen:
    def __init__(self):
        self.data = save.read()
        self.screen = pygame.display.set_mode(self.data['screenSize'])
        pygame.display.set_caption('PyUNO')
        self.running = True

    def quit(self):
        self.running = False

class Achievement():
  def __init__(self, name, description, icon, achieved, achievedDate):
    super().__init__()
    self.icon = icon
    self.image = pygame.image.load(icon).convert_alpha()
    self.name = name
    self.description = description
    self.achieved = False
    self.achievedDate = None
  
class AchievementList():
  def __init__(self):
    super().__init__()
    self.achievements = [
                      Achievement(name = '첫 승리', description = '싱글 플레이어 대전에서 승리', icon = 'victory_image/victory1.png', achieved = False, achievedDate=None),
                      Achievement(name = '지역 탐험가', description = '스토리 모드에서 각 지역별 승리', icon = 'victory_image/victory2.png', achieved = False, achievedDate=None),
                      Achievement(name = '스피드 게임', description = '싱글 플레이어 게임에서 10턴 안에 승리', icon = 'victory_image/victory3.png', achieved = False, achievedDate=None),
                      Achievement(name = '숫자만으로', description = '기술 카드를 단 한번도 사용하지 않고 승리', icon = 'victory_image/victory4.png', achieved = False, achievedDate=None),
                      Achievement(name = '역전승', description = '다른 플레이어가 UNO를 선언한 뒤에 승리', icon = 'victory_image/victory5.png', achieved = False, achievedDate=None),
                      Achievement(name = '1명쯤이야', description = '멀티 플레이어 1명과의 대전에서 승리', icon = 'victory_image/victory6.png', achieved = False, achievedDate=None),
                      Achievement(name = '2명도 가능해', description = '멀티 플레이어 2명과의 대전에서 승리', icon = 'victory_image/victory7.png', achieved = False, achievedDate=None),
                      Achievement(name = 'UNO 고수', description = '멀티 플레이어 3명과의 대전에서 승리', icon = 'victory_image/victory8.png', achieved = False, achievedDate=None),
                      ]
  
class AchievementScreen(Screen):
    def __init__(self):
        super().__init__()
        self.achievementSystem = AchievementList()
        self.font = pygame.font.SysFont('malgungothicsemilight', 14)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.quitButton = Button(280, 20, 40, 40, "Q", self.screen, self.quitScreen)

    def quitScreen(self):
        self.running = False
          
    def draw(self):
        y = 10
        temp = 0
        for achievement in self.achievementSystem.achievements[:8]:
            icon = pygame.transform.scale(achievement.image, (50, 50))
            name = achievement.name
            description = achievement.description
            date = achievement.achievedDate

            # 배경 사각형
            #rect = pygame.Rect(20, y, self.width/2 - 40, self.height/4 -40)
            #pygame.draw.rect(self.screen, (255, 255, 255), rect)

            if temp == 4:
                y = 10

            if temp < 4:
            # 업적 아이콘
                self.screen.blit(icon, (15, y+20))

                # 업적 이름
                nameText = self.font.render(name, True, (0, 0, 0))
                self.screen.blit(nameText, (65, y+10))

                # 업적 설명
                descriptionText = self.font.render(description, True, (0, 0, 0))
                self.screen.blit(descriptionText, (65, y+35))
                
                if self.data["Achievement"][temp] == "T": # 업적 달성하면
                    dateText = self.font.render('달성됨', True, (0, 0, 0))
                else:
                    dateText = self.font.render('달성되지 않음', True, (0, 0, 0))
                    
                self.screen.blit(dateText, (65, y+60))
            elif temp >= 4:
    
        #y = 10
        #for achievement in self.achievementSystem.achievements[4:]:

            #icon = pygame.transform.scale(achievement.image, (50, 50))
            #name = achievement.name
            #description = achievement.description
            
            # 배경 사각형
            #rect = pygame.Rect(self.width - 20 - (self.width/2-40), y, self.width/2 - 40, self.height/4 -40)
            #pygame.draw.rect(self.screen, (255, 255, 255), rect)

                # 업적 아이콘
                self.screen.blit(icon, (325, y+20))

                # 업적 이름
                name_text = self.font.render(name, True, (0, 0, 0))
                self.screen.blit(name_text, (375, y+10))

                # 업적 설명
                description_text = self.font.render(description, True, (0, 0, 0))
                self.screen.blit(description_text, (375, y+35))
            
                if self.data["Achievement"][temp] == "T": # 업적 달성하면
            # 업적 달성 일자
                    dateText = self.font.render('달성됨', True, (0, 0, 0))
                else:
                    dateText = self.font.render('달성되지 않음', True, (0, 0, 0))
            
                self.screen.blit(dateText, (375, y+60))

            y += 100
            temp += 1

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill([255, 255, 255])
            self.draw()
            self.quitButton.process()
            
            pygame.display.update()


class MapScreen(Screen):
    def __init__(self):
        super().__init__()
        # self.screen = self.data['screenSize']
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        self.areaSize = self.data['screenSize'][0] // 4
        self.mapImage = pygame.transform.scale(pygame.image.load("map_image/map.png"), (self.data['screenSize'][0], self.data['screenSize'][1]))
        self.area1 = pygame.transform.scale(pygame.image.load("map_image/stage1.png"), (self.areaSize, self.areaSize))
        self.area2 = pygame.transform.scale(pygame.image.load("map_image/stage2.png"), (self.areaSize, self.areaSize))
        self.area3 = pygame.transform.scale(pygame.image.load("map_image/stage3.png"), (self.areaSize, self.areaSize))
        self.area4 = pygame.transform.scale(pygame.image.load("map_image/stage4.png"), (self.areaSize, self.areaSize))
        
        self.area1Lock = pygame.transform.scale(pygame.image.load("map_image/stage1Lock.png"), (self.areaSize, self.areaSize))
        self.area2Lock = pygame.transform.scale(pygame.image.load("map_image/stage2Lock.png"), (self.areaSize, self.areaSize))
        self.area3Lock = pygame.transform.scale(pygame.image.load("map_image/stage3Lock.png"), (self.areaSize, self.areaSize))
        self.area4Lock = pygame.transform.scale(pygame.image.load("map_image/stage4Lock.png"), (self.areaSize, self.areaSize))

      
        self.areas = [
              (self.width // 4 * 0.5, self.height // 4 * 0.1),
              (self.width // 4 * 2.5, self.height // 4 * 0.5),
              (self.width // 4 * 0.7, self.height // 4 * 1.9),
              (self.width // 4 * 2.7, self.height // 4 * 2.2)
          ]
        

        self.mapRect = self.mapImage.get_rect()
        self.area1Rect = self.area1.get_rect(topleft = self.areas[0])
        self.area2Rect = self.area2.get_rect(topleft = self.areas[1])
        self.area3Rect = self.area3.get_rect(topleft = self.areas[2])
        self.area4Rect = self.area4.get_rect(topleft = self.areas[3])

        self.stageAButton = Button(100, 5, 50, 40, 'A', self.screen, self.showStageA)
        self.stageBButton = Button(450, 50, 50, 40, 'B', self.screen, self.showStageB)
        self.stageCButton = Button(100, 200, 50, 40, 'C', self.screen, self.showStageC)
        self.stageDButton = Button(450, 250, 50, 40, 'D', self.screen, self.showStageD)
        self.nomalButton= Button(20, 310, 100, 40, "Nomal", self.screen, self.nomal)
        self.aButton = Button(20, 360, 100, 40, "A", self.screen, self.a)

        self.buttons = []

        self.buttons.append(self.stageAButton)
        self.buttons.append(self.stageBButton)
        self.buttons.append(self.stageCButton)
        self.buttons.append(self.stageDButton)

        self.smallFont = pygame.font.SysFont('Arial', 18)
        self.textSelect = self.smallFont.render("[v]", True, (0, 0, 100))

        self.quitButton = Button(15, 15, 60, 40, "quit", self.screen, self.quit)
    
    def nomal(self):
        self.checkUser = 'nomal'

    def a(self):
        self.checkUser = 'a'
    
    #TODO 스테이지별 ComputerPlayer를 상속받는 객체 만들고 수정
    def showStageA(self):
        computerList = []
        for i in range(0, 1):
            computerList.append(ComputerPlayerA('computer' + str(i + 1)))
        if self.checkUser == 'nomal':
            SingleGameScreen(HumanPlayer('player'), computerList,'a').run()
        elif self.checkUser == 'a':
            SingleGameScreen(HumanPlayer('player'), computerList,'a').run()
        self.data = save.read()
        self.running = False
       
    
    def showStageB(self):
        computerList = []
        for i in range(0, 3):
            computerList.append(ComputerPlayer('computer' + str(i + 1)))
        if self.checkUser == 'nomal':
            SingleGameScreen(HumanPlayer('player'), computerList,'b').run()
        elif self.checkUser == 'a':
            SingleGameScreen(HumanPlayer('player'), computerList,'b').run()
        self.data = save.read()
        self.running = False

    def showStageC(self):
        computerList = []
        for i in range(0, 2):
            computerList.append(ComputerPlayer('computer' + str(i + 1)))
        if self.checkUser == 'nomal':
            SingleGameScreen(HumanPlayer('player'), computerList,'c').run()
        elif self.checkUser == 'a':
            SingleGameScreen(HumanPlayer('player'), computerList,'c').run()
        self.data = save.read()
        self.running = False

    def showStageD(self):
        computerList = []
        for i in range(0, 1):
            computerList.append(ComputerPlayer('computer' + str(i + 1)))
        if self.checkUser == 'nomal':
            SingleGameScreen(HumanPlayer('player'), computerList,'d').run()
        elif self.checkUser == 'a':
            SingleGameScreen(HumanPlayer('player'), computerList,'d').run()
        self.data = save.read()
        self.running = False

    def quit(self):
        self.running = False
    
    def draw(self):
        self.screen.blit(self.mapImage, (0, 0))
        for i in range(4):
          self.screen.blit(eval(f"self.area{i+1}Lock"), self.areas[i])
        
        if self.data['stageClear'][0] == 'T':
          self.screen.blit(eval("self.area1"), self.areas[0])
        if self.data['stageClear'][1] == 'T':
          self.screen.blit(eval("self.area2"), self.areas[1])
        if self.data['stageClear'][2] == 'T':
          self.screen.blit(eval("self.area3"), self.areas[2])
        if self.data['stageClear'][3] == 'T':
          self.screen.blit(eval("self.area4"), self.areas[3])

          
    def askStart(self):
        # 창 생성
        dialog_x = 400
        dialog_y = 100
        dialog = pygame.Surface((dialog_x, dialog_y))
        dialog.fill((255, 255, 255))
      
        # 텍스트 출력
        font = pygame.font.SysFont('Arial', 30)
        text = font.render("Do you want to Battle in this Stage?", True, (0, 0, 0))
        textRect = text.get_rect(center = (dialog_x // 2, dialog_y // 2))
        dialog.blit(text, textRect)
      
        # 버튼 생성
        acceptButton = pygame.Rect(dialog_x/4, dialog_y*2/3, 50, 20)
        refuseButton = pygame.Rect(dialog_x*2/3, dialog_y*2/3, 50, 20)
        pygame.draw.rect(dialog, (0, 0, 0), acceptButton)
        pygame.draw.rect(dialog, (0, 0, 0), refuseButton)
      
        acceptButtonText = font.render("Yes", True, (255, 255, 255))
        acceptButtonTextRect = acceptButtonText.get_rect(center = acceptButton.center)
        dialog.blit(acceptButtonText, acceptButtonTextRect)
      
        refuseButtonText = font.render("No", True, (255, 255, 255))
        refuseButtonTextRect = refuseButtonText.get_rect(center = refuseButton.center)
        dialog.blit(refuseButtonText, refuseButtonTextRect)
      
        dialogRect = dialog.get_rect(center = self.screen.get_rect().center)
        self.screen.blit(dialog, dialogRect)             
        
        while True:
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if acceptButtonTextRect.collidepoint(event.pos):
                  return True
                    
                elif refuseButton.collidepoint(event.pos):
                  return False

          pygame.display.update()
       
                      
    # 이전 stage 깨지 못한경우 경고창              
    #def alert(self, message):
    #  font = pygame.font.SysFont('Arial', 36)
    #  text = font.render(message, True, (255, 0, 0))
    #  self.screen.blit(text, (self.width/2 - text.get_width()/2, self.height/2 - text.get_height()/2))
    #  pygame.display.update()
      

    def run(self):
  
        self.draw()
        
        temp = 0
        buttonIndex = 0
        selectPos = (self.buttons[buttonIndex].getX(), self.buttons[buttonIndex].getY())

        self.running = True
        while self.running:
            showButtonCount = 0
            for i in self.data['stageClear']:
                if i == 'T':
                    showButtonCount += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == self.data['keyControl'][1] or pygame.key.name(event.key) == self.data['keyControl'][3]: #화살표 아래, 오른쪽 버튼을 눌렀을 때
                        temp = temp + 1
                        buttonIndex = temp % showButtonCount
                        selectPos = (self.buttons[buttonIndex].getX(), self.buttons[buttonIndex].getY())


                    elif pygame.key.name(event.key) == self.data['keyControl'][0] or pygame.key.name(event.key) == self.data['keyControl'][2]: #화살표 위, 왼쪽 버튼을 눌렀을 떄
                        temp = temp - 1
                        buttonIndex = temp % showButtonCount
                        selectPos = (self.buttons[buttonIndex].getX(), self.buttons[buttonIndex].getY())

                    elif pygame.key.name(event.key) == self.data['keyControl'][4]: # Enter키 
                        self.askStart()
                        if True:
                          self.buttons[buttonIndex].runFunction()
                        else:
                          self.draw()
                
                # 마우스 클릭으로 지역 선택
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     mousePos = pygame.mouse.get_pos()
                #     if self.area1Rect.collidepoint(mousePos):
                #       if self.data['stageclear'][] == 'T':
                #         # self.askStart(1)
                        
                #         self.showStageA
                                                                                                                                   
                #     elif self.area2Rect.collidepoint(mousePos):    
                #       if self.data['stageclear'][1] == 'T':
                #         self.askStart(2)
                #       else:
                #         self.alert("You must Stage A Clear!")
                #         pygame.display.update()
                #         pygame.time.delay(2000) 
                #         self.draw()
                        
                    #elif self.area4Rect.collidepoint(mousePos):  
                        #self.askStart(4)
            
            i = 0
            
            for c in self.data['stageClear']:
                if c == 'T':
                    self.buttons[i].process()                  
                i += 1
            
            self.screen.blit(self.textSelect, selectPos)
            self.nomalButton.process()
            self.aButton.process()
            
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
        self.settingButton = Button(30, 280, 140, 40, "setting", self.screen)
        self.quitButton = Button(30, 350, 140, 40, "quit", self.screen, pygame.quit)
        self.storyButton = Button(190, 210, 140, 40, "story", self.screen)
        self.achievementsButton = Button(190, 280, 180, 40, "achievements", self.screen)
        self.MultyButton = Button(190, 350, 140, 40, "multy", self.screen)

        self.buttons.append(self.startButton)
        self.buttons.append(self.settingButton)
        self.buttons.append(self.quitButton)
        self.buttons.append(self.storyButton)
        self.buttons.append(self.achievementsButton)
        self.buttons.append(self.MultyButton)
    
    def showMulty(self):
        multy = MultyPlayScreen()
        multy.run()
        self.data = save.read()
        self.screen = pygame.display.set_mode(self.data['screenSize'])
        sound.playBackground1()

    def showSetting(self):
        settingMenu = SettingScreen()
        settingMenu.run()
        self.data = save.read()
        self.screen = pygame.display.set_mode(self.data['screenSize'])
        sound.playBackground1()

    def showAhiement(self):
        achievementScreen = AchievementScreen()
        achievementScreen.run()
        self.data = save.read()
    
    def showInGame(self):
        inGame = LobbyScreen()
        inGame.run()
        sound.playBackground1()
        self.data = save.read()
    
    def showMap(self):
        map = MapScreen()
        map.run()
        sound.playBackground1()
        self.data = save.read()
    
    def run(self):

        self.settingButton.setOnClickFunction(self.showSetting)
        self.startButton.setOnClickFunction(self.showInGame)
        self.storyButton.setOnClickFunction(self.showMap)
        self.achievementsButton.setOnClickFunction(self.showAhiement)
        self.MultyButton.setOnClickFunction(self.showMulty)

        temp = 0
        buttonIndex = 0
        selectPos = self.buttons[0].getPos()
        isShowHelp = False

        sound.playBackground1()

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == self.data['keyControl'][1] or pygame.key.name(event.key) == self.data['keyControl'][3]: #화살표 아래, 오른쪽 버튼을 눌렀을 때
                        temp = temp + 1
                        buttonIndex = temp % len(self.buttons)
                        selectPos = self.buttons[buttonIndex].getPos()


                    elif pygame.key.name(event.key) == self.data['keyControl'][0] or pygame.key.name(event.key) == self.data['keyControl'][2]: #화살표 위, 왼쪽 버튼을 눌렀을 떄
                        temp = temp - 1
                        buttonIndex = temp % len(self.buttons)
                        selectPos = self.buttons[buttonIndex].getPos()

                    elif pygame.key.name(event.key) == self.data['keyControl'][4]:
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
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.font = pygame.font.SysFont('Arial', 35)

        self.textScreenSize = self.font.render("screen size:", True, [255, 255, 255])
        self.textColorBlindness = self.font.render("color blindness:", True, [255, 255, 255])

        self.buttons = []

        self.screenSizeSmallButton = Button(30, 50, 140, 40, "650X400", self.screen, self.smallScreen)
        self.screenSizeMiddleButton = Button(180, 50, 140, 40, "700X450", self.screen, self.middleScreen)
        self.screenSizeLargeButton = Button(330, 50, 140, 40, "750X500", self.screen, self.largeScreen)

        self.screenColorBlindnessOn = Button(30, 145, 140, 40, "on", self.screen, self.blindnessOn)
        self.screenColorBlindnessOff = Button(180, 145, 140, 40, "off", self.screen, self.blindnessOff)

        self.saveButton = Button(self.width - 150, self.height - 100, 140, 40, "save", self.screen, self.saveData)
        self.exitButton = Button(self.width - 150, self.height - 50, 140, 40, "exit", self.screen, self.quitScreen)

        self.resetButton = Button(self.width - 150, 50, 140, 40, "reset", self.screen, self.resetData)
        
        self.keyUpLabel = Button(30,200, 140, 40, "Up", self.screen)
        self.keyDownLabel = Button(30,250, 140, 40, "Down", self.screen)
        self.keyLeftLabel = Button(30,300, 140, 40, "Left", self.screen)
        self.keyRightLabel = Button(30, 350, 140, 40, "Right", self.screen)
        self.keyEnterLabel = Button(330, 200, 140, 40, "Enter", self.screen)
        
        self.soundUpButton = Button(330, 250, 140, 40, "vol up", self.screen, sound.volumeUp)
        self.soundDownButton = Button(330, 300, 140, 40, "vol down", self.screen, sound.volumeDown)

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
        self.buttons.append(self.soundUpButton)
        self.buttons.append(self.soundDownButton)

        self.clicked=False

    def blindnessOn(self):
        self.data['colorBlindness'] = 'on'

    def blindnessOff(self):
        self.data['colorBlindness'] = 'off'
    
    def smallScreen(self):
        self.data['screenSize'] = [650, 400]

    def middleScreen(self):
        self.data['screenSize'] = [700, 450]

    def largeScreen(self):
        self.data['screenSize'] = [750, 500]

    def saveData(self):
        save.write(self.data)

    def quitScreen(self):
        self.running = False

    def resetData(self):
        self.data['screenSize'] = [700, 450]
        self.data['keyControl'][0] = 'up'
        self.data['keyControl'][1] = 'down'
        self.data['keyControl'][2] = 'left'
        self.data['keyControl'][3] = 'right'
        self.data['keyControl'][4] = 'return'
        self.data['colorBlindness'] = 'off'
        save.write(self.data)

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
            keyUpBox = pygame.Rect(180,200, 140, 40)
            keyDownBox = pygame.Rect(180,250, 140, 40)
            keyLeftBox = pygame.Rect(180,300, 140, 40)
            keyRightBox = pygame.Rect(180,350, 140, 40)
            keyEnterBox = pygame.Rect(480,200, 140, 40)

            
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
                        #self.setting.write(self.data)
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

            self.screen.blit(keyUpText, (180,200))
            self.screen.blit(keyDownText, (180,250))
            self.screen.blit(keyLeftText, (180,300))
            self.screen.blit(keyRightText, (180,350))
            self.screen.blit(keyEnterText, (480,200))

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
        SingleGameScreen(HumanPlayer(self.nameText), computerList).run()
        self.data = save.read()
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
    
    def __init__(self, player, computerList, stage = None):
        super().__init__()
        self.stage = stage
        self.playerName = player.name
        self.player = player
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
        self.haveWinner = False
        self.winner = None
        self.stageCCount = 1
        self.smallFont = pygame.font.SysFont('Arial', 18)
        self.textSelect = self.smallFont.render("[●]", True, (0, 0, 100))
        self.tap = []
        self.tapX = 0
        self.tapY = 0
        self.checkUseAbility = False

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()


        self.escButtons = []

        self.quitButton= Button(20, (self.height // 4), 160, 40, 'quit game', self.screen, self.quitScreen)
        saveButton = Button(20, (self.height // 4) * 2, 100, 40, 'setting', self.screen, self.showSetting)

        self.escButtons.append(self.quitButton)
        self.escButtons.append(saveButton)
        
        self.buttons = []

        self.unoButton = Button(10, self.data['screenSize'][1] - 50, 100, 35, 'UNO', self.screen, self.uno)
        self.drawCardButton = Button(self.data['screenSize'][0] // 4 - 80, self.data['screenSize'][1] // 3,60, 35, 'add', self.screen, self.drawCard)

    def endTurn(self):
        self.index = self.index + self.turnNum
        self.nowTurnPlayer = self.nowTurnList[self.index % len(self.nowTurnList)]
        self.comTurnTime = pygame.time.get_ticks() + self.nowTurnPlayer.time
        self.humanStartTime = pygame.time.get_ticks()
        self.deck.addCard(self.discard)

        #내 선택
        self.tap[0][0] = self.drawCardButton
        self.tap[1] = self.nowTurnPlayer.handsOnCard
        self.tap[2][0] = self.unoButton


        if self.stage == 'c':
            self.stageCCount += 1
            if self.stageCCount % 5 == 0:
                r = random.randint(1, 4)
                if r == 1:
                    if self.discard.cards[0].color != 'None':
                        self.discard.cards[0].color = 'red'
                    else:
                        self.discard.cards[0].color = 'red'
                        self.discard.cards[0].value = '0'
                elif r == 2:
                    if self.discard.cards[0].color != 'None':
                        self.discard.cards[0].color = 'blue'
                    else:
                        self.discard.cards[0].color = 'blue'
                        self.discard.cards[0].value = '0'
                elif r == 3:
                    if self.discard.cards[0].color != 'None':
                        self.discard.cards[0].color = 'green'
                    else:
                        self.discard.cards[0].color = 'green'
                        self.discard.cards[0].value = '0'
                elif r == 4:
                    if self.discard.cards[0].color != 'None':
                        self.discard.cards[0].color = 'yellow'
                    else:
                        self.discard.cards[0].color = 'yellow'
                        self.discard.cards[0].value = '0'



    def drawCard(self):
        if self.stage == 'd':
            self.nowTurnPlayer.addCard(self.deck.drawCard())
            self.nowTurnPlayer.addCard(self.deck.drawCard())
        self.nowTurnPlayer.addCard(self.deck.drawCard())
        self.endTurn()


    def quitScreen(self):
        self.running = False

    def ability(self, ability):
        self.checkUseAbility = True
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
            self.haveWinner = True
            self.winner = self.nowTurnPlayer
            self.endTurn()
        elif self.discard.cards[0].value == 'changeColor':
            if isinstance(self.nowTurnPlayer, HumanPlayer):
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
                r = random.randint(1, 4)
                if r == 1:
                    if self.discard.cards[0].color != 'None':
                        self.discard.cards[0].color = 'red'
                    else:
                        self.discard.cards[0].color = 'red'
                        self.discard.cards[0].value = '0'
                elif r == 2:
                    if self.discard.cards[0].color != 'None':
                        self.discard.cards[0].color = 'blue'
                    else:
                        self.discard.cards[0].color = 'blue'
                        self.discard.cards[0].value = '0'
                elif r == 3:
                    if self.discard.cards[0].color != 'None':
                        self.discard.cards[0].color = 'green'
                    else:
                        self.discard.cards[0].color = 'green'
                        self.discard.cards[0].value = '0'
                elif r == 4:
                    if self.discard.cards[0].color != 'None':
                        self.discard.cards[0].color = 'yellow'
                    else:
                        self.discard.cards[0].color = 'yellow'
                        self.discard.cards[0].value = '0'

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
        self.data = save.read()
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
            if len(self.nowTurnPlayer.handsOnCard) == 2:
                self.nowTurnPlayer.checkUno = True
            else:
                self.nowTurnList[0].addCard(self.deck.drawCard())

    def run(self):

        handsOnColor = [0, 120, 0]
        listColor = [30, 30, 30]
        isInputEsc = False
        endSound = True

        #게임 시작시 실행되는 내용
        font = pygame.font.SysFont('Arial', 25)
        winFont = pygame.font.SysFont('Arial', 60)
        self.deck.createDeck()
        self.player.handsOnCard = self.player.handsOnCard + self.deck.prepareCard()
        self.deck.shuffle()
        self.nowTurnList = [self.player] + self.computerList 
        self.discard.addCard(self.deck.drawCard())

        self.nowTurnPlayer = self.nowTurnList[self.index % len(self.nowTurnList)]
        self.comTurnTime = pygame.time.get_ticks() + self.nowTurnPlayer.time
        self.humanStartTime = pygame.time.get_ticks()
        
        self.tap.append([self.drawCardButton])
        self.tap.append(self.nowTurnPlayer.handsOnCard)
        self.tap.append([self.unoButton])
        selectPos = (self.tap[self.tapY][self.tapX].getX(), self.tap[self.tapY][self.tapX].getY())
        temp1 = 0
        temp2 = 0

        clock = pygame.time.Clock()

        sound.playBackground2()

        for i in range(len(self.computerList)):#카드 분배
            self.computerList[i].dealCards(self.deck)

        if self.stage == 'b':
            for i in range(2, len(self.deck.cards)):
                self.nowTurnList[i % len(self.nowTurnList)].handsOnCard.append(self.deck.cards[i])
                

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and isinstance(self.nowTurnPlayer, HumanPlayer):
                    for i in range(len(self.nowTurnPlayer.handsOnCard)):
                        if self.nowTurnPlayer.handsOnCard[i].canInsert and self.nowTurnPlayer.handsOnCard[i].isClicked(pygame.mouse.get_pos()):
                            sound.playClickSound()
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
                    if pygame.key.name(event.key) == self.data['keyControl'][1]:
                        temp1 += 1
                        self.tapX = 0
                        temp2 = 0
                        self.tapY = temp1 % 3
                        selectPos = (self.tap[self.tapY][self.tapX].getX(), self.tap[self.tapY][self.tapX].getY())
                    elif pygame.key.name(event.key) == self.data['keyControl'][3]: #화살표 아래, 오른쪽 버튼을 눌렀을 때
                        temp2 += 1
                        self.tapX = temp2 % len(self.tap[self.tapY])
                        selectPos = (self.tap[self.tapY][self.tapX].getX(), self.tap[self.tapY][self.tapX].getY())
                    elif pygame.key.name(event.key) == self.data['keyControl'][0]:
                        temp1 -= 1
                        self.tapX = 0
                        temp2 = 0
                        self.tapY = temp1 % 3
                        selectPos = (self.tap[self.tapY][self.tapX].getX(), self.tap[self.tapY][self.tapX].getY())
                    elif pygame.key.name(event.key) == self.data['keyControl'][2]: #화살표 위, 왼쪽 버튼을 눌렀을 떄
                        temp2 -= 1
                        self.tapX = temp2 % len(self.tap[self.tapY])
                        selectPos = (self.tap[self.tapY][self.tapX].getX(), self.tap[self.tapY][self.tapX].getY())
                    elif pygame.key.name(event.key) == self.data['keyControl'][4]:
                        if self.tapY == 0:
                            self.drawCard()
                        elif self.tapY == 2:
                            self.uno()
                        elif self.tapY == 1:
                            if self.nowTurnPlayer.handsOnCard[self.tapX].canInsert:
                                sound.playClickSound()
                                self.nowTurnPlayer.pushCard(self.tapX, self.discard)
                                if isinstance(self.discard.cards[0], AbilityCard):
                                    if self.nowTurnPlayer.checkUno == False and len(self.nowTurnPlayer.handsOnCard) == 1:
                                        self.nowTurnPlayer.addCard(self.deck.drawCard())
                                    self.ability(self.discard.cards[0].value)
                                else:
                                    if self.nowTurnPlayer.checkUno == False and len(self.nowTurnPlayer.handsOnCard) == 1:
                                        self.nowTurnPlayer.addCard(self.deck.drawCard())
                                    self.endTurn()
                                self.nowTurnPlayer.checkUno = False


            if self.haveWinner:

                if isinstance(self.winner, HumanPlayer) and self.stage == 'a':
                    self.data['stageClear'][1] = 'T'
                if isinstance(self.winner, HumanPlayer) and self.stage == 'b':
                    self.data['stageClear'][2] = 'T'
                if isinstance(self.winner, HumanPlayer) and self.stage == 'c':
                    self.data['stageClear'][3] = 'T'
                if isinstance(self.winner, HumanPlayer) and self.stage == 'd':
                    self.data['Achievement'][1] = 'T'
                if self.index <= 10:
                    self.data['Achievement'][2] = 'T'
                if self.checkUseAbility:
                    self.data['Achievement'][3] = 'T'
                if len(self.computerList) == 2:
                    self.data['Achievement'][5] = 'T'
                if len(self.computerList) == 3:
                    self.data['Achievement'][6] = 'T'
                if len(self.computerList) == 4:
                    self.data['Achievement'][7] = 'T'
                
                if endSound:
                    if isinstance(self.winner, HumanPlayer):
                        sound.playWinSound()
                        self.data["Achievement"][0] = 'T'
                    elif isinstance(self.winner, ComputerPlayer):
                        sound.playLoseSound()
                    endSound = False

                text = ''
                quitButton = Button(self.data['screenSize'][0] // 2 - 50, self.data['screenSize'][1] // 3 * 2, 100, 35, 'quit', self.screen, self.quitScreen)
                self.screen.fill([255, 255, 255])
                #if(len(self.deck.cards) == 0):
                #    text = 'The game ended in a tie'
                #    winText = winFont.render(text, True, (0, 0, 0))
                #    self.screen.blit(winText, (self.data['screenSize'][0] // 2 - 300, self.data['screenSize'][1] // 3))
                #else:
                #for p in self.nowTurnList:
                #    if len(p.handsOnCard) == 0:
                text = 'winner : ' + self.winner.name
                winText = winFont.render(text, True, (0, 0, 0))
                self.screen.blit(winText, (self.data['screenSize'][0] // 2 - 150, self.data['screenSize'][1] // 3))
                quitButton.process()
                pygame.display.flip()
                save.write(self.data)

            elif isInputEsc:
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
                    if len(p.handsOnCard) <= 0:
                        self.haveWinner = True
                        self.winner = p
                
                #if len(self.deck.cards) <= 0:
                #        self.haveWinner = True

                #컴퓨터의 턴
                if isinstance(self.nowTurnPlayer, ComputerPlayer):
                    if pygame.time.get_ticks() - self.comTurnTime > 800:
                        if self.nowTurnPlayer.playTurn(self.discard, self.changeColor):
                            if self.nowTurnPlayer.checkUno == True and len(self.nowTurnPlayer.handsOnCard) == 1:
                                if isinstance(self.discard.cards[0], AbilityCard):
                                        self.ability(self.discard.cards[0].value)
                                else:
                                    self.endTurn()
                                self.drawCard()
                            else:
                                if isinstance(self.discard.cards[0], AbilityCard):
                                        self.ability(self.discard.cards[0].value)
                                else:
                                    self.endTurn()
                        else:
                            self.drawCard()
                        self.nowTurnPlayer.checkUno = False


                elif isinstance(self.nowTurnPlayer, HumanPlayer):#플레이어의 턴
                    
                    self.nowTurnPlayer.checkCanInsert(self.discard, self.changeColor)

                    #내 턴 일때 출력
                    elapsedTime = (pygame.time.get_ticks() - self.humanStartTime) / 1000
                    timer = font.render('time : ' + str(int(self.nowTurnPlayer.totalTime - elapsedTime)), True, (255, 255, 255))
                    self.screen.blit(timer,(10, 10))

                    if self.nowTurnPlayer.totalTime - elapsedTime <= 0:#타임 오버
                        self.drawCard()

                    self.drawCardButton.process()
                    self.screen.blit(self.textSelect, selectPos)
                

                pygame.display.flip()

class MultyPlayScreen(Screen):
    def __init__(self):
        super().__init__()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.buttons = [] 

        self.serverButton = Button(self.data['screenSize'][0] // 2, self.data['screenSize'][1] // 3, 140, 40, "server", self.screen, self.showServerScreen)
        self.joinButton= Button(self.data['screenSize'][0] // 2, self.data['screenSize'][1] // 3 + 60, 140, 40, "client", self.screen, self.showClientScreen)
        self.exitButton = Button(self.data['screenSize'][0] // 2, self.data['screenSize'][1] // 3 + 120, 140, 40, "quit", self.screen, self.quit)

        self.buttons.append(self.serverButton)
        self.buttons.append(self.joinButton)
        self.buttons.append(self.exitButton)
    
    def quit(self):
        self.running = False
    
    def showServerScreen(self):
        host = hostScreen()
        host.run()

    def showClientScreen(self):  
        client = ClientScreen()
        client.run()
                    
    def run(self):

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False

            self.screen.fill(self.data['backgroundColor'])

            for btn in self.buttons:
                btn.process()

            pygame.display.flip()

class hostScreen(Screen):
    def __init__(self):
        super().__init__()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.nameText = 'player'
        self.password = ''
        self.ip = socket.gethostbyname(hostName)
        self.insertCoutn = 1
        self.players = []
        self.buttons = [] 

        self.quitButton = Button(30, self.data['screenSize'][1] - 70, 140, 40, 'quit', self.screen, self.quit)
        self.addButton = Button(180, self.data['screenSize'][1] - 70, 140, 40, 'add', self.screen, self.addComputer)
        self.delButton = Button(330, self.data['screenSize'][1] - 70, 140, 40, 'del', self.screen, self.delComputer)

        self.buttons.append(self.quitButton)
        self.buttons.append(self.addButton)
        self.buttons.append(self.delButton)

        self.font = pygame.font.Font(None, 32)
        self.rect = pygame.Rect([(self.data['screenSize'][0] // 4) * 3 + 2, 0], [self.data['screenSize'][0], self.data['screenSize'][1]])
        self.ipText = self.font.render("IP : " + self.ip, True, (255, 255, 255)) 
        self.hostText = self.font.render("host", True, (255, 255, 255)) 
        self.noneText = self.font.render('none', True, (255, 255, 255)) 
        self.computerText = self.font.render('computer', True, (255, 255, 255)) 
        self.passwordText= self.font.render('password', True, (255, 255, 255)) 
        self.inputBox = pygame.Rect(30, self.data['screenSize'][1] // 5 - 40, 140, 32)
        self.inputBoxPassword = pygame.Rect(30, self.data['screenSize'][1] // 5 + 40, 140, 32)
    
    def addComputer(self):
        if self.insertCoutn < 5:
            self.players.append(ComputerPlayer('computer' + str(self.insertCoutn)))
            self.insertCoutn += 1
    
    def delComputer(self):
        if self.insertCoutn > 1:
            self.players.pop()
            self.insertCoutn -= 1
    
    def run(self):

        color_inactive = pygame.Color('lightskyblue3')
        color = color_inactive
        active = False
        activeP = False

        server.start()

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
                    if self.inputBoxPassword.collidepoint(event.pos):
                        activeP = not active
                    else:
                        activeP = False
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            self.nameText = self.nameText[:-1]
                        else:
                            self.nameText += event.unicode
                    if activeP:
                        if event.key == pygame.K_BACKSPACE:
                            self.password = self.password[:-1]
                        else:
                            self.password += event.unicode

            self.screen.fill(self.data['backgroundColor'])
            pygame.draw.rect(self.screen, [30, 30, 30], self.rect)

            for btn in self.buttons:
                btn.process()

            self.screen.blit(self.ipText, (30, self.data['screenSize'][1] // 5))
            self.screen.blit(self.passwordText, (260, self.data['screenSize'][1] // 5 + 40))
            
            #이름 입력 칸
            txt_surface = self.font.render(self.nameText, True, color)
            width = max(200, txt_surface.get_width()+10)
            self.inputBox.w = width
            # Blit the text.
            self.screen.blit(txt_surface, (self.inputBox.x+5, self.inputBox.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(self.screen, color, self.inputBox, 2)

            txt_surfaceP = self.font.render(self.password, True, color)
            widthPassword = max(200, txt_surfaceP.get_width()+10)
            self.inputBoxPassword.w = widthPassword
            # Blit the text.
            self.screen.blit(txt_surfaceP, (self.inputBoxPassword.x+5, self.inputBoxPassword.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(self.screen, color, self.inputBoxPassword, 2)

            #오른쪽 플레이어 확인
            self.screen.blit(self.hostText, ((self.data['screenSize'][0] // 5) * 4, 10))
            for i in range(0,4):
                if i < len(self.players):
                    if isinstance(self.players[i], ComputerPlayer):
                        self.screen.blit(self.computerText, ((self.data['screenSize'][0] // 5) * 4, (self.data['screenSize'][1] // 5) * (i + 1)))
                else:
                    self.screen.blit(self.noneText, ((self.data['screenSize'][0] // 5) * 4, (self.data['screenSize'][1] // 5) * (i + 1)))

            pygame.display.flip()
        
        server.stop()

class ClientScreen(Screen):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 32)
        self.inputText = '127.0.0.1'
        self.inputBox = pygame.Rect(30, self.data['screenSize'][1] // 5 - 40, 140, 32)

        self.connectButton = Button(30, self.data['screenSize'][1] // 5 * 4, 140, 40, 'connect', self.screen, self.connect)

        self.buttons = [] 
        self.buttons.append(self.connectButton)

    def connect(self):
        client.connect()
    
    def run(self):

        color_inactive = pygame.Color('lightskyblue3')
        color = color_inactive
        active = False
        client.host = self.inputText

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
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            self.inputText = self.inputText[:-1]
                            client.host = self.inputText
                        else:
                            self.inputText += event.unicode
                            client.host = self.inputText

            self.screen.fill(self.data['backgroundColor'])

            for btn in self.buttons:
                btn.process()

            #IP 입력 칸
            txt_surface = self.font.render(self.inputText, True, color)
            width = max(200, txt_surface.get_width()+10)
            self.inputBox.w = width
            # Blit the text.
            self.screen.blit(txt_surface, (self.inputBox.x+5, self.inputBox.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(self.screen, color, self.inputBox, 2)


            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    b = MultyPlayScreen()
    b.run()

