import pygame
from pygame.locals import *
import random

class Card(pygame.sprite.Sprite):
    def __init__(self, colour_id = 0, rank_id = 0, card_name="", card_width=80, card_height=127): #colour_id, rank_id
        super().__init__()
      
        self.rank_id = rank_id
        self.colour_id = colour_id
        self.card_width=card_width
        self.card_height=card_height
        # self.fillColors = { 'normal' : "#ffffff",
        #                    "hover" : "#666666", 
        #                    "pressed" : "#333333"}
        # self.buttonSurface = pygame.Surface((self.card_width, self.card_height))
        # self.buttonRect = pygame.Rect(self.x, self.y, self.card_width, self.card_height)
        # self.selected = False
        if self.rank_id == 10:
            self.rank = "Skip"
           
        elif self.rank_id == 11:
            self.rank = "Draw_two"
      
        elif self.rank_id == 12:
            self.rank = "Reverse"

        #numbered cards
        if 0 <= self.rank_id <= 9:
            self.rank = self.rank_id
            self.point = self.rank_id 
        if self.colour_id == 0:
            self.colour = "red"
        elif self.colour_id == 1:
            self.colour = "green"
        elif self.colour_id == 2:
            self.colour = "blue"
        elif self.colour_id == 3:
            self.colour = "yellow"
        elif self.colour_id==4: #wild
            self.colour="black"
            self.rank_id = 13
            self.rank = "Wild"
            self.point = 50
            self.colour_choice = "rainbow" 
        elif self.colour_id==5: # wild draw card
            self.colour="black"
            self.rank_id = 14
            self.rank = "Wild_draw_four"
            self.point = 50
            self.colour_choice = "rainbow"
        if card_name=="":
            self.name=str(self.colour.lower())+str(self.rank_id)
        else:
            self.name=card_name

        self.image = pygame.transform.smoothscale(pygame.image.load("uno_cards_image/uno_card-"+self.name+".jpg"), (card_width, card_height)) 
        self.hover_image = self.image.copy()
        self.original_image = self.image
        self.mouse_pos = None
        pygame.draw.rect(self.hover_image, (255, 255, 0), self.hover_image.get_rect(), 6)
        self.rect = self.image.get_rect()
    def __repr__(self):
        return str(self.colour) + " " + str(self.rank) + " Points:" + str(self.point)

    def process(self):
     

        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        self.image = self.hover_image if self.hover else self.original_image
      
        # if self.hover and mouse_pos == self.mouse_pos:
        #     self.count += 1
         
        
        # else:
        #     self.count = 0
        self.mouse_pos = mouse_pos
     

        #screen.blit(self.buttonSurface, self.buttonRect)

class preparegame():
    def __init__(self):
        self.decklist=[]
        self.player_dict = {}
        self.create_deck()
        self.prepare_cards()

    def create_deck(self):
        for colour_id in range(0, 6):
            # adding 4 wild cards 
            if colour_id == 4:
                self.decklist.append(Card(colour_id, rank))
                self.decklist.append(Card(colour_id, rank))
                self.decklist.append(Card(colour_id, rank))
                self.decklist.append(Card(colour_id, rank))
                
             
            #adding 4 wild draw cards
            elif colour_id == 5:
                self.decklist.append(Card(colour_id, rank))
                self.decklist.append(Card(colour_id, rank))
                self.decklist.append(Card(colour_id, rank))
                self.decklist.append(Card(colour_id, rank))
               

            if colour_id < 4:
                for rank in range(0, 10): 
                    if rank==0:
                        self.decklist.append(Card(colour_id, rank))
                    if 1<=rank<=12:
                        self.decklist.append(Card(colour_id, rank))
                        self.decklist.append(Card(colour_id, rank))

                for rank in range(10, 13):
                    self.decklist.append(Card(colour_id, rank))
                    self.decklist.append(Card(colour_id, rank))

    def prepare_cards(self):
 
        for player in range(0, #self.no_of_players
        2):
            hand = []
            for i in range(0, 7):
                a = random.choice(self.decklist)
                hand.append(a)
                self.decklist.remove(a)
            #append hand list of cards to players list to form a list of all players hands
            self.player_dict[player]=hand
        random.shuffle(self.decklist)
        # after deck initilisation, you get dictionary of players and cards + drawpile 

