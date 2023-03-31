class Piece:
    def __init__(self, row, col, id):
        self.row = row
        self.col = col
        self.id = id
        self.king = False
        
        if self.id < 13:
            self.direction = -1
            self.color = "orange"
        else:
            self.direction = 1
            self.color = "blue"
        
    def make_king(self):
        self.king = True
    
    def move(self, row, col):
        self.row = row
        self.col = col
    
    def __repr__(self):
        return str(self.id)