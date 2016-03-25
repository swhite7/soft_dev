# Contains the method to setup a game
# Each game has a fixed way of starting and so this can be contained within a method
# Stephen White
from __future__ import print_function
from card_game_objects import *
import random
from copy import deepcopy
import sys


'''
Function to set up a game. This involves reading in the game parameters and cards to use
and filling the players and card holder objects
'''


def game_setup():

    # Reading in the game parameters and decks of cards
    game_params = read_game_parameters()
    main_deck, player_deck, supplement = read_card_list()
    
    # Due to how Python handles referencing, need to create copies of the player_deck variable for both players
    human_deck = deepcopy(player_deck)
    computer_deck = deepcopy(player_deck)
    # Instantiating player and card holder objects for the game using parameters and decks read in
    human_player = Player('Player One', game_params[0], human_deck, [], [], game_params[1], [])
    computer_player = Player('Player Computer', game_params[0], computer_deck, [], [], game_params[1], [])
    card_holder = Card_Holder('Card Holder', [], game_params[2], supplement, main_deck)
    
    
    # Need to fill the active area of the card_holder with cards to buy
    for i in range(card_holder.get_activeSize()):
        card = card_holder.get_deck().pop()
        card_holder.get_active().append(card)

    # Need to fill the hands of each players with cards from their deck    
    for x in range(human_player.get_handsize()):
        h_card = human_player.get_deck().pop()
        human_player.get_hand().append(h_card)
     
    for x in range(computer_player.get_handsize()):
        c_card = computer_player.get_deck().pop()
        computer_player.get_hand().append(c_card)

    return human_player, computer_player, card_holder



# Want method to read in the game parameters text file
def read_game_parameters():

    # Reads in the game parameters text file
    # These must be in a specific order so only numerical values of parameters should change
    with open('game_parameters.txt','r') as param_text:
        param_contents = param_text.read() 
    split_contents = [x.strip() for x in param_contents.split(',')]
    
    health = int(split_contents[1])
    handsize = int(split_contents[3])
    no_of_available_cards = int(split_contents[5])
    
    game_parameters = [health,handsize,no_of_available_cards]
    return game_parameters
    
    
# Want method to read in the list of cards and assign them to the right decks
def read_card_list():


    game_deck = []
    player_deck = []
    supplement_deck = []
    
    # The cards in the text file have a value 0,1 or 2 corresponding to which deck they belong to
    # 0 is the main deck, 1 is the player's starting deck and 2 is the supplement deck
    with open('list_of_cards.txt','r') as card_list: 
        #reading dummy line
        card_list.readline()
        for line in card_list:
            split_line = [x.strip() for x in line.split(',')]
            card = Card(split_line[1],(int(split_line[2]),int(split_line[3])), int(split_line[4]))
            if int(split_line[5]) == 0:
                game_deck.extend(int(split_line[0])*[card])
            elif int(split_line[5]) == 1:
                player_deck.extend(int(split_line[0])*[card])
            elif int(split_line[5]) == 2:
                supplement_deck.extend(int(split_line[0]) * [card])
    
    # Shuffling main deck
    random.shuffle(game_deck)


    
    return game_deck,player_deck,supplement_deck
      
# Function to ask the user if they want to start a game and set the options (opponent behaviour)
def new_game():
    play_game_input = str.upper(raw_input('Do you want to play a game? (Y to play): '))
    confirmed_game = (play_game_input) == 'Y'
    
    # A game will only be played if 'y' or 'Y' is entered, else the program quits
    if confirmed_game:
        behav_choice = str.upper(raw_input("Do you want an aggressive (A) opponent or an acquisative (Q) opponent: "))
        aggressive = (behav_choice == 'A')
        human, computer, holder = game_setup()
    else:
        sys.exit()
    return human,computer,holder,aggressive

# The core loop of the game
def play_game(continue_game,human, computer,holder,aggressive):
    
    # Loop of the game is: human player turn, check for win, computer turn, check for win and repeat
    while continue_game:
        player_turn(human, computer, holder)
        continue_game = win_conditions(human, computer, holder, continue_game) 
        # This is required so that the computer turn is not played if the game has already been won by the human player           
        if continue_game:
            computer_turn(human, computer, holder, aggressive)
            continue_game = win_conditions(human, computer, holder, continue_game) 
    return

# Code for the human player's turn        
def player_turn(player,computer,card_holder):
    
    
    # Set initial money and attack values to zero
    money = 0
    attack = 0

        # Want to be in a loop to be the player turn until it is broken by ending the turn
    while True:

            # Printing current healths
        print("\nPlayer Health %s" % player.get_health())
        print("Computer Health %s" % computer.get_health())
            
            # Printing the cards that the player currently has in their hand
        print("\nYour Hand")
        index = 0
        for card in player.get_hand():
            print("[%s] %s" % (index, card))
            index = index + 1
    
            # Printing the active cards that the player currently has 
        print("\nYour Active Cards")
        for card in player.get_active():
            print(card)

            # Printing current money and attack values
        print("\nYour Values")
        print("Money %s, Attack %s" % (money, attack))
            
            # Prompt user for an action
        print("\nChoose Action: (P = play all, [0-n] = play that card, B = Buy Card, A = Attack, E = end turn)")

        player_action = str.upper(raw_input("Enter Action: "))
        print(player_action)

            # Code for if the player selects "play all" option
        if player_action == 'P':

                # Check if hand is empty or not
            if(len(player.get_hand())>0):
                    # Add each card in the player's hand to their active area
                for x in range(0, len(player.get_hand())):

                    card = player.get_hand().pop()
                    player.get_active().append(card)
                    money = money + card.get_money()
                    attack = attack + card.get_attack()
                                 
            # Code for if a player wants to play a specific card
        elif player_action.isdigit():

                # Number input must correspond to an available card
            if( int(player_action) < len(player.get_hand())):
                player.get_active().append(player.get_hand().pop(int(player_action)))
                
                for card in player.get_active():
                    money = money + card.get_money()
                    attack = attack + card.get_attack()
            else:
                print('Invalid option')
            
            # Code for if a player wants to buy cards
        elif (player_action == 'B'):
                
                # Only keep looping if the player has money left to spend
            while money > 0:

                    # Printing the cards that can be bought
                print("Available Cards")
                ind = 0
                for card in card_holder.get_active():
                    print("[%s] %s" % (ind,card))
                    ind = ind + 1
                    
                    # Prompting user to choose an action about buying cards
                print("Choose a card to buy [0-n], S for supplement, E to end buying")
                buying_action = str.upper(raw_input("Choose option: "))

                    # If the user wants to buy a supplement
                if buying_action == 'S':   
                        # Can only buy if there are supplement cards remaining
                    if len(card_holder.get_supplement()) > 0:
                            # Player must have enough money
                        if money >= card_holder.get_supplement()[0].cost:
                                # Removing cost from player money and adding a supplement to the player's discard pile
                            money = money - card_holder.get_supplement()[0].cost
                            player.get_discard().append(card_holder.get_supplement().pop())
                            print("Supplement Bought")

                        else:
                            print("insufficient money to buy")
                    else:
                        print("no supplements left")
                    
                    # If the user wants to buy a specific card
                elif buying_action.isdigit():
                        # Number entered must correspond to an available card
                    if int(buying_action) < len(card_holder.get_active()):
                        # Player must have enough money available
                        if money >= card_holder.get_active()[int(buying_action)].cost:
                            # Removing cost from payer money and adding the chosen card to player's discard pile
                            money = money - card_holder.get_active()[int(buying_action)].cost
                            player.get_discard().append(card_holder.get_active().pop(int(buying_action)))
                                # Drawing a card from the main deck to repopulate the available cards if possible
                            if( len(card_holder.get_deck()) > 0):

                                card = card_holder.get_deck().pop()
                                card_holder.get_active().append(card)
    
                            else:

                                card_holder.set_activeSize(card_holder.get_activeSize() - 1) 
              
                            print("Card bought")
                        else:
                            print("insufficient money to buy")
                    else:
                        print("enter a valid index number")

                    # If the user wants to finish buying cards
                elif buying_action == 'E':
                    break;
                else:
                    print("Invalid option")

            # Code for if the player chooses to attack their opponent
            # This takes the attack value built up from active cards and subtracts it from enemy health
        elif player_action == 'A':

            computer.set_health(computer.get_health() - attack)
            attack = 0


            # Code for if the player chooses to end their turn
        elif player_action == 'E':
                # if the player's hand contains cards then they are sent to their discard pile
            if (len(player.get_hand()) >0 ):
                for x in range(0, len(player.get_hand())):
                    player.get_discard().append(player.get_hand().pop())
                
                # If the player has any active cards then they are also sent to their discard pile
            if (len(player.get_active()) >0 ):
                for x in range(0, len(player.get_active())):
                    player.get_discard().append(player.get_active().pop())

                # The player's hand is repopulated from their deck
            for x in range(0, player.get_handsize()):
                    # When the player's deck is empty their discard pile is shuffled and transferred to the deck
                if len(player.get_deck()) == 0:
                    random.shuffle(player.get_discard())
                    player.set_deck(player.get_discard())
                    player.set_discard([])
                    # Draws a card from the player's deck for their hand
                card = player.get_deck().pop()
                player.get_hand().append(card)
            break
            # Accounts for invalid input
        else:
            print('Invalid option')
            
# Code for computer player's turn
def computer_turn(player,computer,card_holder,aggres):
    
    money = 0
    attack = 0
    
    # The computer player will always play all of the cards in their hand
    # This for loop will move all hand cards to the active area
    for x in range(0, len(computer.get_hand())):
        card = computer.get_hand().pop()
        computer.get_active().append(card)
        money = money + card.get_money()
        attack = attack + card.get_attack()

    # Reports the value of the cards that the computer player has played
    print(" Computer player values attack %s, money %s" % (attack, money))
    # Attacking the human player
    print(" Computer attacking with strength %s" % attack)
    player.set_health(player.get_health() - attack)
    attack = 0

    # Printing the player healths after attack
    print("\nPlayer Health %s" % player.get_health())
    print("Computer Health %s" % computer.get_health())

    # Reporting computer player values after attack
    print(" Computer player values attack %s, money %s" % (attack, money))
    print("Computer buying")

    # Computer player will buy until it has no more money available
    if money > 0:
        continue_buying = True
        templist = []
        print("Starting Money %s and continue_buying %s " % (money, continue_buying))
        while continue_buying:

                # Want to populate a list with cards that the computer player would be able to afford
            templist = []
                # adding a supplement to list if there is any left and if the computer can afford it
            if len(card_holder.get_supplement()) > 0 and card_holder.get_supplement()[0].cost <= money:
                templist.append(("S", card_holder.get_supplement()[0]))
                
                # Adding any of the available cards that the computer can afford to the list
            for intindex in range (0, card_holder.get_activeSize()):
                if card_holder.get_active()[intindex].cost <= money:
                    templist.append((intindex, card_holder.get_active()[intindex]))
                # If there are any affordable cards
            if len(templist) >0:
                highestIndex = 0
                for intindex in range(0,len(templist)):
                        # Filling highestIndex with most expensive cards possible
                    if templist[intindex][1].cost > templist[highestIndex][1].cost:
                        highestIndex = intindex
                        # If more than one card_game_objects have the highest cost
                    if templist[intindex][1].cost == templist[highestIndex][1].cost:
                        # If aggresive computer behaviour then higher attack card_game_objects is prioritised
                        if aggres:
                            if templist[intindex][1].get_attack() >templist[highestIndex][1].get_attack():
                                    highestIndex = intindex
                        else:
                                # if not aggresive then higher money card_game_objects is prioritised
                            if templist[intindex][1].get_attack() >templist[highestIndex][1].get_money():
                                highestIndex = intindex

                card_to_buy = templist[highestIndex][0]
                    
                    #If the card_game_objects being bought is one of the available cards
                if card_to_buy in range(0,5):
                        # Another money check
                    if money >= card_holder.get_active()[int(card_to_buy)].cost:
                            # Removing money and adding card_game_objects to discard pile of computer player
                        money = money - card_holder.get_active()[int(card_to_buy)].cost
                        card = card_holder.get_active().pop(int(card_to_buy))
                        print("Card bought %s" % card)
                        computer.get_discard().append(card)
                            # Repopulating, if possible, the available cards from the main deck
                        if( len(card_holder.get_deck()) > 0):
                            card = card_holder.get_deck().pop()
                            card_holder.get_active().append(card)
                        else:
                            card_holder.set_activeSize(card_holder.get_activeSize() - 1)
                    else:
                        print("Error Occurred")
                else:
                        # If the card_game_objects is not one of the available ones then it must be a supplement
                    if money >= card_holder.get_supplement()[0].cost:
                        money = money - card_holder.get_supplement()[0].cost
                        card = card_holder.get_supplement().pop()
                        computer.get_discard().append(card)
                        print("Supplement Bought %s" % card)
                    else:
                        print("Error Occurred")
            else:
                continue_buying = False
                # Check to see if computer used all its money during buying loop
            if money == 0:
                continue_buying = False
    else:
        print("No Money to buy anything")

        # If the computer has any card_game_objects left in its hand or active then move these to discard pile
    if (len(computer.get_hand()) >0 ):
        for x in range(0, len(computer.get_hand())):
            computer.get_discard().append(computer.get_hand().pop())
    if (len(computer.get_active()) >0 ):
        for x in range(0, len(computer.get_active())):
            computer.get_discard().append(computer.get_active().pop())

        # Repopulate computer hand from its deck, replacing deck with shuffled discard if the deck is empty
    for x in range(0, computer.get_handsize()):
        if len(computer.get_deck()) == 0:
            random.shuffle(computer.get_discard())
            computer.set_deck(computer.get_discard())
            computer.set_discard([])
        card = computer.get_deck().pop()
        computer.get_hand().append(card)
    print("Computer turn ending")

        # Printing available cards and health statuses
    print("Available Cards")
    for card in card_holder.get_active():
        print(card)

    print("Supplement")
    if len(card_holder.get_supplement()) > 0:
        print(card_holder.get_supplement()[0])

    print("\nPlayer Health %s" % player.get_health())
    print("Computer Health %s" % computer.get_health())

# Code to check the win conditions of the game
def win_conditions(player, computer,card_holder, continue_game):
    
    if player.get_health() <= 0:
        continue_game = False
        print("Computer wins")
    elif computer.get_health() <= 0:
        continue_game = False
        print('Player One Wins')
    elif card_holder.get_activeSize() == 0:
        print("No more cards available")

            # If main deck is empty then game ends and whoever has the most health wins
        if player.get_health() > computer.get_health():
            print("Player One Wins on Health")
        elif computer.get_health() > player.get_health():
            print("Computer Wins on Health")
        else:
            # If the game has ended because of empty main deck and players have equal health then see who has best cards
            # This condition has not been implemented yet
            h_play_strength = 0
            c_play_strength = 0
            
            if(len(player.get_hand())>0):
                # Add each card in the player's hand to their total strength

                    card = player.get_hand().pop()
                    player.get_active().append(card)
                    h_play_strength += card.get_money() + card.get_attack()
                    
            if(len(computer.get_hand())>0):
                # Add each card in the computer's hand to their total strength

                    card = computer.get_hand().pop()
                    computer.get_active().append(card)
                    c_play_strength += card.get_money() + card.get_attack()
            
            
            
            if h_play_strength > c_play_strength:
                print("Player One Wins on Card Strength")
            elif c_play_strength > h_play_strength:
                print("Computer Wins on Card Strength")
            else:
                print("Draw")
        continue_game = False
    
    return continue_game
