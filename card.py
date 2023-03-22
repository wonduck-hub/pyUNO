import random
import pygame
import sys
sys.setrecursionlimit(10**6)


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
black = (255, 255, 255)

colors = ["red", "yellow", "green", "blue"]
color_values = [str(i) for i in range(10)] + ["skip", "reverse", "draw2"]
noncolor_values = ["change_color", "defense", "joker"]


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.image = pygame.image.load('card_image/' + self.color + "_" + str(self.value) + ".png")



class Deck:

    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        self.cards = [] # cards 빈 리스트로 초기화
        # 카드 생성하여 cards에 추가
        for color in colors:
            for value in color_values: # 0~9 숫자카드와 색 있는 기술카드
                self.cards.append(Card(color, value))

        for i in range(4):
            for value in noncolor_values: # 색 없는 기술카드 4장
                self.cards.append(Card("None", value))

    def shuffle(self): # cards 리스트 무작위로 섞음
        random.shuffle(self.cards)

    def draw_card(self): # cards에서 가장 앞에 있는 카드 뽑아냄 (player)
        return self.cards.pop(0)

    def add_card(self, card): # 인자로 받은 card를 cards 리스트에 추가
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

    # card = Card('red', 0)
    # screen.blit(card.image, (50, 50))

    bg_color = pygame.Color("green")
    screen.fill(bg_color)
    # screen.blit(card.image)

    # 화면 업데이트
    pygame.display.update()

# Pygame 종료
pygame.quit()

