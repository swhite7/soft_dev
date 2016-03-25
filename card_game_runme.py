# Main script to run the deck-based card_game_objects game_deck
# Stephen White
# March 2016
from __future__ import print_function
# Need to import the two functions required to play a game. One sets up a new game and one runs a full game
from card_game_functions import play_game, new_game


# Main method of program 
if __name__ == '__main__':
    
    # Want to loop the game playing until user has chosen not to play again
    playing = True
    
    while playing:
        
        # Calling function that sets up a new game
        human,computer,holder,aggressive = new_game()
        
        # Tracks whether the game is over or not
        # When someone wins, this changes to false and the play_game function ends
        game_on = True
        # This function contains the core gameplay loop
        play_game(game_on, human,computer,holder,aggressive)
        
        
    
    


        
