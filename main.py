
from checkers.board import Board
from checkers.game import Game

# checkerboard = Board()

# piece = checkerboard.get_piece(0,1)

# # checkerboard.move_piece(piece, 4, 3)

# checkerboard.print_board()

game = Game()

#game.select(2, 1)
#game.select(7, 9)

game.robot.grab_piece((6, 7))
game.robot.drop_in_box()