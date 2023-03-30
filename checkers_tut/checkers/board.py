from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.blue_left = self.orange_left = 12
        self.blue_kings = self.orange_kings = 0
        self.create_board()
    
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def create_board(self):
        orange_ids = 1
        blue_ids = 13
        for row in range(8):
            self.board.append([])
            for col in range(8):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, orange_ids))
                        orange_ids += 1
                    elif row > 4:
                        self.board[row].append(Piece(row, col, blue_ids))
                        blue_ids += 1
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    
    def print_board(self):
        for row in self.board:
            print(row)
            
    def move_piece(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        
        if row == 7 or row == 0:
            piece.make_king()
            if piece.id < 13:
                self.orange_kings += 1
            else:
                self.blue_kings += 1