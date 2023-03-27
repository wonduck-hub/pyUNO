import card
import random
import pygame
from pygame.locals import *


# 버린 카드 클래스
class DiscardPile:
    def __init__(self,deck):
        self.cards = [] 
        self.createPile(deck) 

    def createPile(self,deck): #게임을 시작하기 위해 첫번째 카드 생성
        self.cards = []
        self.cards.append(deck.drawCard())

    def addCard(self, card): 
        self.cards.append(card)


# 플레이어 클래스
class Player:
    def __init__(self, name):
        # 플레이어 패 생성
        self.name = name
        self.handsOnCard = []

    def showHandsOnCard(self):
        for card in self.handsOnCard:
            card.show(self.width // 2, self.height // 2)

    
    #마지막 카드에 기반해 플레이어 패에서 낼 수 있는 카드 리스트 생성
    def playableCard(self, discardPileCard):
        playableCard=[]
        if discardPileCard[-1].color=="None": #마지막 카드가 색이 없는 기술카드일 경우 현재색과 같은 카드 추가
            for card in self.handsOnCard:
                 if card.color == "red": #현재색이 빨강색이라 가정
                    playableCard.append(card)   
        else:
            for card in self.handsOnCard:
                if card.color == discardPileCard[-1].color or card.value == discardPileCard[-1].value or card.color=="None":
                    playableCard.append(card)   
        return playableCard
    
    
                

# 사용자 플레이어 클래스
class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.time=3000
        
       
# 컴퓨터 플레이어 클래스 
class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.time=2000


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("카드 게임")

    bg_color = pygame.Color("green")
    screen.fill(bg_color)


    # 카드덱 생성
    deck = card.Deck()

    human_plyr = HumanPlayer(deck) #사용자 객체 
    pc_plyr = ComputerPlayer(deck) # 컴퓨터 객체

    discardPile = DiscardPile(deck) # 버린 카드 객체
    discardPileCard = discardPile.cards # 버린 카드 리스트


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            


    # Pygame 종료
    pygame.quit()





