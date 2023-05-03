from card import NumberCard, AbilityCard
import random
import pygame
from pygame.locals import *


# 버린 카드 클래스
class DiscardPile:
    def __init__(self):
        self.cards = [] 
        self.font = pygame.font.Font(None, 20)

    def createPile(self,deck): #게임을 시작하기 위해 첫번째 카드 생성
        self.cards = []
        self.cards.append(deck.drawCard())

    def addCard(self, card): 
        self.cards.insert(0, card)

    def show(self, x, y, changeColor, screen):
        self.cards[0].show(x, y)

        if self.cards[0].color != changeColor and self.cards[0].value != 'changeColor':
            changeColor = 'None'

        if changeColor == 'None':
            nowColor = self.font.render(self.cards[0].color, True, (255, 255, 255))
            screen.blit(nowColor, (x + 60, y))
        else:
            nowColor = self.font.render(changeColor, True, (255, 255, 255))
            screen.blit(nowColor, (x + 60, y))
        
    def sendCard(self):
        return self.cards.pop()



# 플레이어 클래스
class Player:
    def __init__(self, name):
        # 플레이어 패 생성
        self.name = name
        self.handsOnCard = []
        self.isWin = False
        self.time = 2000
        self.checkUno = False

    def addCard(self, card):
        card.faceUp = True
        self.handsOnCard.append(card)
    
    def insertCard(self, index):
        result = self.handsOnCard.pop(index)
        return result
    
    
                

# 사용자 플레이어 클래스
class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.totalTime = 30

    def showHandsOnCard(self, x, y):
        for i in range(len(self.handsOnCard)):
            if self.handsOnCard[i].canInsert:
                self.handsOnCard[i].show(x + (i * 50), y - 10)
            else:
                self.handsOnCard[i].show(x + (i * 50), y)
    
    def checkCanInsert(self, discard, changeColor):
        for i in range(len(self.handsOnCard)):
            if discard.cards[0].value == 'changeColor':
                if self.handsOnCard[i].color == changeColor or self.handsOnCard[i].value == discard.cards[0].value or self.handsOnCard[i].color == 'None':
                    self.handsOnCard[i].canInsert = True
                else:
                    self.handsOnCard[i].canInsert = False
            elif discard.cards[0].value == 'joker':
                self.handsOnCard[i].canInsert = True
            elif isinstance(discard.cards[0], NumberCard):
                if self.handsOnCard[i].color == discard.cards[0].color or self.handsOnCard[i].value == discard.cards[0].value or self.handsOnCard[i].color == 'None':
                    self.handsOnCard[i].canInsert = True
                else:
                    self.handsOnCard[i].canInsert = False
            elif isinstance(discard.cards[0], AbilityCard):
                if self.handsOnCard[i].color == discard.cards[0].color or self.handsOnCard[i].color == 'None':
                    self.handsOnCard[i].canInsert = True
                else:
                    self.handsOnCard[i].canInsert = False
    
    def pushCard(self, index, discard):
        discard.addCard(self.insertCard(index))

    def dealCards(self, deck):
        self.handsOnCard += deck.prepareCard()



class HumanPlayerA(HumanPlayer):
    def __init__(self, name):
        super().__init__(name)

    def dealCards(self, deck):
        #150%로 기술카드 뽑기
        for i in range(0, 7):
            r = random.randint(1, 5)
            if r <= 3:
                for i in range(len(deck.cards)):
                    if isinstance(deck.cards[i], AbilityCard):
                        self.handsOnCard.append(deck.cards.pop(i))
                        break
            elif r > 3:
                for i in range(len(deck.cards)):
                    if isinstance(deck.cards[i], NumberCard):
                        self.handsOnCard.append(deck.cards.pop(i))
                        break
       
# 컴퓨터 플레이어 클래스 
class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.font = pygame.font.Font(None, 20)
    
    def dealCards(self, deck):
        self.handsOnCard += deck.prepareCard()

    def showHandsOnCard(self, x, y, screen):
        name = self.font.render(self.name, True, (128, 128, 128))
        num = self.font.render('X' + str(len(self.handsOnCard)), True, (128, 128, 128))
        screen.blit(name, (x, y))
        screen.blit(num, (x + 50, y + 40))
        image = pygame.transform.scale(pygame.image.load("card_image/back.png"), (30, 50))
        screen.blit(image, (x, y + 25))
    
    def playTurn(self, discard, changeColor):
        for i in range(len(self.handsOnCard)):
            if discard.cards[0].value == 'changeColor':
                if self.handsOnCard[i].color == changeColor or self.handsOnCard[i].value == discard.cards[0].value or self.handsOnCard[i].color == 'None':
                    discard.addCard(self.insertCard(i))
                    return True
            elif discard.cards[0].value == 'joker':
                discard.addCard(self.insertCard(i))
                return True
            elif isinstance(discard.cards[0], NumberCard):
                if self.handsOnCard[i].color == discard.cards[0].color or self.handsOnCard[i].value == discard.cards[0].value or self.handsOnCard[i].color == 'None':
                    discard.addCard(self.insertCard(i))
                    return True
            elif isinstance(discard.cards[0], AbilityCard):
                if self.handsOnCard[i].color == discard.cards[0].color or self.handsOnCard[i].color == 'None':
                    discard.addCard(self.insertCard(i))
                    return True
        else:
            return False

class ComputerPlayerA(ComputerPlayer): 
    def __init__(self, name):
        super().__init__(name)

    def dealCards(self, deck):
        #150%로 기술카드 뽑기
        for i in range(0, 7):
            r = random.randint(1, 5)
            if r <= 3:
                for i in range(len(deck.cards)):
                    if isinstance(deck.cards[i], AbilityCard):
                        self.handsOnCard.append(deck.cards.pop(i))
                        break
            elif r > 3:
                for i in range(len(deck.cards)):
                    if isinstance(deck.cards[i], NumberCard):
                        self.handsOnCard.append(deck.cards.pop(i))
                        break



if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("카드 게임")

    bg_color = pygame.Color("green")
    screen.fill(bg_color)




    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            


    # Pygame 종료
    pygame.quit()





