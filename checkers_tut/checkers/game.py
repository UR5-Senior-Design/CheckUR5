from checkers.board import Board

class Game:
    def __init__(self): #(self, win):
        self._init()
        # self.win = win
    
    def update(self):
        # self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = "blue"
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    # row and column are the row and col selected
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col) #move the selected piece to the row and col
            if not result: #if selected piece is invalid
                self.selected = None #reset the selection
                self.select(row, col) #re-select a new row and column

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn: #if valid piece and turn
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True #selected something
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves: #if we selected a piece that is 0 and if the row/col we selected is not a piece
            self.board.move_piece(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == "blue":
            self.turn = "orange"
        else:
            self.turn = "blue"

    def get_board(self):
        return self.board
    
    def ai_move(self, board): #when ai makes move it will return new board after move
        self.board = board    #updates game with new board object
        self.change_turn()
