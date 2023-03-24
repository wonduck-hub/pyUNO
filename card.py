import random
import pygame

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

colors = ["red", "yellow", "green", "blue"]
color_values = [str(i) for i in range(10)] + ["skip", "reverse", "draw2"]
noncolor_values = ["change_color", "defense", "joker"]


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.width = 100
        self.height = 150  
        
        image_path = f"card_image/{color}_{value}.png"
        self.image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
        
        self.rect = self.image.get_rect() # 카드의 사각형 영역

    def draw(self, x, y): # 위치 정보 인자로 받아 카드 그리기
        screen.blit(self.image, (x, y))

    def is_clicked(self, x, y): # 카드 선택되었는지 확인
      if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
        return True
      else:
        return False
      
    def select(self): # 카드 선택한 상태로 변경
       pygame.draw.rect(screen, white, (self.rect, self.width, self.height), 5)
      
    def deselect(self): # 카드 선택 해제 상태로 변경
      pygame.draw.rect(screen, )
      
      
class NumberCard(Card):
    def __init__(self, color, value):
        super().__init__(color, value)
        
        
class AbilityCard(Card):
    def __init__(self, color, ability):
        super().__init__(color, ability)
        self.ability = ability
      
class Deck:

    def __init__(self):
        self.cards = [] # 카드 덱
        self.createDeck() # 카드 덱 초기화

    def createDeck(self):
        self.cards = [] # cards 빈 리스트로 초기화
        # 카드 생성하여 cards에 추가
        for color in colors:
            for value in color_values: # 0~9 숫자카드와 색 있는 기술카드
                self.cards.append(Card(color, value))

        for i in range(4):
            for value in noncolor_values: # 색 없는 기술카드 4장
                self.cards.append(Card("None", value))
        return self.cards

        
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
    
    # 숫자 카드 객체 생성
    # number_card = NumberCard("red", 1)
    # 특수 능력 카드 객체 생성
    # ability_card = AbilityCard("None", "joker")
    # ability_card1 = AbilityCard("green", "skip")
    # 카드 그리기
    # number_card.draw(50, 50)
    # ability_card.draw(100, 100)
    # ability_card1.draw(200, 200)
    
    # 화면 업데이트
    pygame.display.update()

# Pygame 종료
pygame.quit()

