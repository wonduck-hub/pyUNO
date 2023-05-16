import pygame

class SoundManager():
    def __init__(self):
        pygame.mixer.init()
        self.click = pygame.mixer.Sound("./sound/playSound/click.mp3")
        self.win = pygame.mixer.Sound("./sound/playSound/win.mp3")
        self.lose = pygame.mixer.Sound("./sound/playSound/lose.mp3")

    def playBackground2(self):
        pygame.mixer.music.load("./sound/backgroundSound/backgroundSound2.mp3")
        pygame.mixer.music.play(-1)

    def playBackground1(self):
        pygame.mixer.music.load("./sound/backgroundSound/backgroundSound1.mp3")
        pygame.mixer.music.play(-1)

    def playClickSound(self):
        self.click.play()

    def playWinSound(self):
        self.win.play()

    def playLoseSound(self):
        self.lose.play()
    
    def volumeUp(self):
        v = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(v + 0.1)
    
    def volumeDown(self):
        v = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(v - 0.1)

sound = SoundManager()