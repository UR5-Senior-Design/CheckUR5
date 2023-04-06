from checkers.board import Board
from checkers.robot import Robot
from checkers.piece import Piece

# note: robot will be the ORANGE checker pieces

class Game:
    def __init__(self):
        self._init()
        #self.win = win
    
    def __del__(self):
        print("Destructor for Game called.")
        del self.robot
    
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

    def get_winner(self):
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
        
        is_valid = self.selected and piece == 0 and (row, col) in self.valid_moves
        print(f"In move selection with ({row}, {col}) {is_valid}")
        
        if self.selected and piece == 0 and (row, col) in self.valid_moves: #if we selected a piece that is not empty/0 and if the row/col we selected is not a piece
            print(f"Moving robot")
            
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

    def get_board(self):
        return self.board
    
    def ai_move(self, new_board): #when ai makes move it will return new board after move
        # get the position of the piece the ai decided to move and move command robot to move it to the new position
        # by comparing the old board with the new board
        moved = {} # store the pieces that have moved between both old and new board into a dictionary whose key is its (id, color) and value is a set that stores a dictionary of its old and new positions
        
        # loop and find all the pieces that are different/moved from the previous board and store them
        for row in range(0,8):
            for col in range(0,8):
                old_piece = self.board.get_piece(row, col)
                new_piece = new_board.get_piece(row, col)
                
                # the only difference will be a number and a 0 or a 0 and a number, since validate moves will only allow movement to empty spaces
                # if the old value is a value while the new value is a 0, that means that thats the position the piece moved from
                if isinstance(old_piece, Piece) and not isinstance(new_piece, Piece): # the old piece is a value that changed to 0 (this is the position it moved from)
                    key = (old_piece.id, old_piece.color)
                    if key not in moved:
                        moved[key] = {}
                        
                    moved[key]["old"] = (old_piece.row, old_piece.col)
                elif isinstance(new_piece, Piece) and not isinstance(old_piece, Piece): # the old piece is a 0 and the new piece is a value (this is the position it moved to)
                    key = (new_piece.id, new_piece.color)
                    
                    if key not in moved:
                        moved[key] = {}
                    
                    moved[key]["new"] = (new_piece.row, new_piece.col)
        
        # print list of pieces that moved
        print(f"\tAI Play - pieces that changed: {moved}")
        
        # physically move all the pieces from the old board to match the state of the new board
        # move all orange pieces first (there should only be one orange piece moved)
        for key in moved:
            color = key[1]
            if color == "orange":
                key_id = key[0]
                old_pos = moved[key]["old"]
                new_pos = moved[key]["new"]
                
                self.robot.grab_piece(old_pos)
                self.robot.drop_piece(new_pos)

                print(f"\tMoved orange piece {key_id} from {old_pos} to {new_pos}")
        
        # move all of the blue pieces
        # if the differing piece is a "blue" player, that means we've eaten/skipped over a piece, so move the robot to drop those pieces into the collection box
        for key in moved:
            color = key[1]
            if color == "blue":
                key_id = key[0]
                old_pos = moved[key]["old"]

                self.robot.grab_piece(old_pos)
                self.robot.drop_in_box() 

                print(f"\tRemoved blue piece {key_id} from {old_pos}")
        
        self.board = new_board    #updates game with new board object
        self.change_turn()
