from checkers.game import Game
from checkers.minimax.algorithm import minimax
import time

MINIMAX_DEPTH = 4

# start running the checkers game from here
def main():
    run = False # set state of the game
    game = Game()

    print(f"Welcome to CheckUR5!\n\nHere are the commands you can type and send:\n")
    userInput = input(f"\tstart - start the game\n\tquit - quit the game\n")

    if (userInput == 'start'):
        run = True
    elif (userInput == 'quit'):
        run = False
    else: # lol this logic isn't checking for bad commands after the else so it would just default to exit
        print(f"ERROR:Please enter a valid command!\n\nHere are the commands you can type and send:\n")
        userInput = input(f"\tstart - start the game\n\tquit - quit the game\n")

    while run:
        
        winner = game.get_winner()
        if winner != None:
            if winner == "orange":
                print(f"The UR5 Robot won the game!")
            else:
                print(f"The Player won the game!")
            
            # TODO: maybe give option to reset and start the game again here???
            run = False
        # robot's turn
        elif game.turn == "orange":
            value, new_board = minimax(game.get_board(), MINIMAX_DEPTH, "orange", game)

            print("UR5 Robot's turn actions: \n")
            game.ai_move(new_board) # set robot's move decision and move robot
        # human player's turn
        elif game.turn == "blue":
            # TODO: add turn timeout after 20 seconds
            # timeout = 20 # 20 seconds to make a turn
            player_input = input("Player's turn, press A to end turn or B to get more options")

            if player_input == "A":
                pass
                # TODO: some computer vision logic here maybe?
            elif player_input == "B":
                print("MORE GAME OPTIONS:")
                player_input = input(f"\n\treset - reset the game\n\tquit - quit the game\n")
                if player_input == "reset":
                    pass
                    # TODO: add interaction to reset the game
                    # lol idk how to incorporate this
                elif player_input == "quit":
                    print(f"Thank you for playing! :)")
                    run = False

            # indicate the moves/removes human has made
            print(f"Player's turn actions: \n")
    

main()