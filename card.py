import random
import pygame
from utils.saveManager import SettingManager

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

color_values = [str(i) for i in range(10)]
noncolor_values = ["changeColor", "defense", "joker"]


class Card:
    def __init__(self, color, value, screen):
        self.x = 0
        self.y = 0
        self.screen = screen
        self.color = color
        self.value = value
        self.width = 50
        self.height = 80  
        self.faceUp = True # 카드 뒤집어져 있는지 여부, 기본값 = back
        
        imagePath = f"./card_image/{color}_{value}.png"
        self.image = pygame.transform.scale(pygame.image.load(imagePath), (self.width, self.height))
        
        self.rect = self.image.get_rect() # 카드의 사각형 영역
        
    def show(self, x, y): # 위치 정보 인자로 받아 카드 그리기
        self.x = x
        self.y = y
        if self.faceUp:
            self.screen.blit(self.image, (self.x, self.y))
        else:
            self.image = pygame.transform.scale(pygame.image.load("card_image/back.png"), (self.width, self.height))
            self.screen.blit(self.image, (self.x, self.y))
        
    def isClicked(self, pos):
        return self.rect.collidepoint(pos)

    def flip(self): # 카드 앞면 뒷면 전환
      self.faceUp = not self.faceUp
      
      
class NumberCard(Card):
    def __init__(self, color, value, screen):
        super().__init__(color, value, screen)
        
        
class AbilityCard(Card):
    def __init__(self, color, screen, ability = None):
        super().__init__(color, screen, ability = None)
        self.ability = ability
      
class Deck:

    def __init__(self, screen):
        self.colors = ["red", "yellow", "green", "blue"]
        self.cards = [] # 카드 덱
        self.selectedCard = None
        self.screen = screen
        self.data = SettingManager()
        
    def createDeck(self):
        self.cards = [] # cards 빈 리스트로 초기화
        # 카드 생성하여 cards에 추가
        # 나중에 수정
        for color in self.colors:
            for value in color_values: # 0~9 숫자카드
                self.cards.append(NumberCard(color, value, self.screen))

        #나중에 기술카드 추가
        #self.cards.append(AbilityCard(color, self.screen))
        #self.cards.append(AbilityCard(color, self.screen))
        #self.cards.append(AbilityCard(color, self.screen))
        #self.cards.append(AbilityCard(color, self.screen))
        #        
        #self.cards.append(AbilityCard(color, self.screen))
        #self.cards.append(AbilityCard(color, self.screen))
        #self.cards.append(AbilityCard(color, self.screen))
        #self.cards.append(AbilityCard(color, self.screen))

        #self.cards.append(AbilityCard(color, self.screen))
        #self.cards.append(AbilityCard(color, self.screen))
        #self.cards.append(AbilityCard(color, self.screen))
        #self.cards.append(AbilityCard(color, self.screen))

        #self.cards.append(AbilityCard(color, self.screen))
        #self.cards.append(AbilityCard(color, self.screen))
        #self.cards.append(AbilityCard(color, self.screen))
        #self.cards.append(AbilityCard(color, self.screen))

        #self.cards.append(AbilityCard(color, self.screen))

        
    def prepareCard(self): # 게임 시작 전 플레이어에게 card 분배 및 카드더미 섞기
      handsOnCard = [] # 플레이어가 들고 있는 카드
      for i in range(7):
        a = random.choice(self.cards)
        handsOnCard.append(a)
        self.cards.remove(a)
      return handsOnCard
      
    def shuffle(self):
      random.shuffle(self.cards)

    def drawCard(self): # 카드덱에서 카드 뽑아냄 (player)
        return self.cards.pop(0)

    def addCard(self, card): # 인자로 받은 card를 cards 리스트에 추가
        self.cards.append(card)

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("카드 게임")


    pygame.display.update()


    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        bg_color = pygame.Color("green")
        screen.fill(bg_color)
        pos = pygame.mouse.get_pos()
        
        # 예시코드
        # 숫자 카드 객체 생성
        number_card = NumberCard("blue", 1)
        # 특수 능력 카드 객체 생성
        ability_card = AbilityCard("None", "joker")
        ability_card1 = AbilityCard("green", "skip")
        # 카드 그리기
        number_card.show(50, 50)
        ability_card.show(100, 100)
        ability_card1.flip()
        ability_card1.show(200, 200)
        
        # 화면 업데이트
        pygame.display.update()

    # Pygame 종료
    pygame.quit()


