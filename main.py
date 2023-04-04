
from checkers.board import Board
from checkers.game import Game

all_arucos = {13: [3, 4]}

checkerboard = Board()
print("old board:")
checkerboard.print_board()

# checkerboard.piece_db[12].make_king()

checkerboard.get_piece(5, 0).make_king()

print("new king board:")
checkerboard.print_board()

checkerboard.update_board(all_arucos)

print("updated board")
checkerboard.print_board()

# piece = checkerboard.get_piece(0,1)

# # checkerboard.move_piece(piece, 4, 3)

# checkerboard.print_board()

# game = Game()

# game.select(2, 1)
# game.select(3, 2)