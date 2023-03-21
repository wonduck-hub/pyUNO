import pygame
from utils.saveManager import settingManager
from utils.button import Button

class Screen:
    def __init__(self):
        self.setting = settingManager()
        self.data = self.setting.read()
        self.screen = pygame.display.set_mode(self.data['screenSize'])
        self.backgourndColor = self.data['backgroundColor']

class StartScreen(Screen):
    def __init__(self):
        super().__init__()
        self.setting = settingManager()
        self.data = self.setting.read()
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

        self.buttons = []
        self.startButton = Button(30, 210, 140, 40, "start",self.screen)
        self.menuButton = Button(30, 280, 140, 40, "menu", self.screen)
        self.quitButton = Button(30, 350, 140, 40, "quit", self.screen, pygame.quit)

        self.buttons.append(self.startButton)
        self.buttons.append(self.menuButton)
        self.buttons.append(self.quitButton)

    
    def run(self):
        temp = 0
        buttonIndex = 0
        selectPos = self.buttons[0].getPos()
        isShowHelp = False

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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
            
            self.screen.fill(self.backgourndColor)
            
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
                        
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    pygame.init()
    start = StartScreen()
    start.run()