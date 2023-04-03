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
            if piece.color == "orange":
                self.orange_kings += 1
            else:
                self.blue_kings += 1
    
    def winner(self):
        if self.blue_left <= 0:
            return "orange"
        elif self.orange_left <= 0:
            return "blue"
        
        return None
        
                
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == "blue":
                    self.blue_left -= 1
                else:
                    self.orange_left -= 1
         
    def get_valid_moves(self, piece):
        moves = {} #store the move as the key, 
        # (4,5): [(3,4)] = jumped through 3,4 to get through 4,5
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        
        if piece.color == "blue" or piece.king: #need to change to id
            moves.update(self._traverse_left(row - 1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row-3, -1), -1, piece.color, right))
        
        if piece.color == "orange" or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, 8), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, 8), 1, piece.color, right))
        
        return moves
    
    '''
    start, stop: for the for-loop
    step: going up or down/ left or right (top or bot diagonal) when traversing the diagonal
    skipped: lets us know if we have skipped any pieces yet (if yes, we can only move to certain squares )
    '''
    def _traverse_left(self, start, stop, step, color, left, skipped=[]): #traverses the left diagonal
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.get_piece(r, left)
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, 8)
                    
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            
            left -= 1
        
        return moves
    

    def _traverse_right(self, start, stop, step, color, right, skipped=[]): #traverses the right diagonal
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= 8:
                break
            
            current = self.get_piece(r, right)
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, 8)
                    
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            
            right += 1

        return moves