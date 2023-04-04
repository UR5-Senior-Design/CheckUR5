from checkers.board import Board
from checkers.robot import Robot

# note: robot will be the ORANGE checker pieces

class Game:
    def __init__(self):
        self._init()
        #self.win = win
    
    def update(self):
        # self.board.draw(self.win)
        # self.draw_valid_moves(self.valid_moves)
        pass

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = "orange"
        self.valid_moves = {}
        self.robot = Robot(arduino_port='/dev/ttyUSB0', robot_ip="192.168.1.102")

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    # row and column are the row and col selected
    def select(self, row, col):
        if self.selected:
            result = self.move_selection(row, col) #move the selected piece to the row and col
            
            if not result: #if selected piece is invalid
                self.selected = None #reset the selection
                self.select(row, col) #re-select a new row and column

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn: #if valid piece and turn
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            
            print(f"Selected piece: {self.selected.row} {self.selected.col}")
            print(f"\tValid moves: {self.valid_moves}")
            
            return True #selected something
            
        return False

    def move_selection(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves: #if we selected a piece that is not empty/0 and if the row/col we selected is not a piece
            # robot arm moves selected/grabbed piece if it is the turn of the robot and drops it at its new location
            if self.turn == "orange":
                self.robot.grab_piece((self.selected.row, self.selected.col))
                self.robot.drop_piece((row, col))
            
            self.board.move_piece(self.selected, row, col)
            
            print(f"Move selected piece to: {row} {col}")
            
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