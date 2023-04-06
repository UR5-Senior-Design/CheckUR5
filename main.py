from checkers.board import Board
from checkers.game import Game
from minimax.algorithm import minimax


game = Game()

new_board = Board()

new_board.print_board()
print("\n")

# checkerboard.move_piece(piece, 4, 3)

# checkerboard.print_board()

value, new_board = minimax(game.get_board(), 2, "orange", game)
game.ai_move(new_board)

new_board.print_board()
print("\n")


#lol i thought that this would move the human piece but it didnt!
#the computer do be making it's own moves tho
# piece = checkerboard.get_piece(5,4)
# new_board.move_piece(piece, 4, 5)

# value, new_board = minimax(game.get_board(), 2, "orange", game)
# game.ai_move(new_board)

# new_board.print_board()

game.select(5,4)
game.select(4,5)
new_board.print_board()
print("\n")