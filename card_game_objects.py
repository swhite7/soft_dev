# A card object is basic instrument of playing the game with associated cost, attack value and money value
from __future__ import print_function 
class Card(object):

    # Constructor with some default values
    def __init__(self, name, values=(0, 0), cost=1):
        self.name = name
        self.cost = cost
        self.values = values

    # Method to return description of all card properties when object is printed as string
    def __str__(self):
        return 'Name %s costing %s with attack %s and money %s' % (self.name, self.cost, self.values[0], self.values[1])

    # Method to return attack value of card
    def get_attack(self):
        return self.values[0]
    # Method to return money value of card
    def get_money(self):
        return self.values[1]
    
    


class Player(object):
    
    #Constructor defining a player
    
    def __init__(self, name, health, deck, hand, active, handsize, discard):
        
        self.name = name
        self.health = health
        self.deck = deck
        self.hand = hand
        self.active = active
        self.handsize = handsize
        self.discard = discard
    # Need get and set methods for all properties    
    def get_name(self):
        return self.name   
    def get_health(self):
        return self.health
    def get_deck(self):
        return self.deck
    def get_hand(self):
        return self.hand
    def get_active(self):
        return self.active
    def get_handsize(self):
        return self.handsize
    def get_discard(self):
        return self.discard
    
    def set_name(self,new_name):
        self.name = new_name  
        return 
    def set_health(self,new_health):
        self.health = new_health
        return
    def set_deck(self,new_deck):
        self.deck = new_deck
        return
    def set_hand(self,new_hand):
        self.hand = new_hand
        return
    def set_active(self,new_active):
        self.active = new_active
        return
    def set_handsize(self,new_handsize):
        self.handsize = new_handsize
        return
    def set_discard(self,new_discard):
        self.discard = new_discard
        return
    
    
class Card_Holder(object):
    
    def __init__(self,name, active, activeSize, supplement,deck):
        self.name = name
        self.active = active
        self.activeSize = activeSize
        self.supplement = supplement
        self.deck = deck
    # Need get and set methods for all properties    
    def get_name(self):
        return self.name
    def get_active(self):
        return self.active
    def get_activeSize(self):
        return self.activeSize
    def get_supplement(self):
        return self.supplement
    def get_deck(self):
        return self.deck
    
    def set_name(self,new_name):
        self.name = new_name
        return
    def set_active(self,new_active):
        self.active = new_active
        return
    def set_activeSize(self,new_activeSize):
        self.activeSize = new_activeSize
        return
    def set_supplement(self,new_supplement):
        self.supplement = new_supplement
        return
    def set_deck(self,new_deck):
        self.deck = new_deck
        return






