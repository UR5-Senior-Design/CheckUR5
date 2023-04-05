from copy import deepcopy #allows you to make a copy of an object & modify it without affecting the original & vice versa

def minimax(position, depth, max_player, game):
    #position = (board object) where we current position we are in
    #depth = (int) how far am i extending this tree?
    #max_player = (bool) are we maximizing(TRUE) or are we minimizing(FALSE)
    #game = (game object) will allow us to call the game functions

    if depth == 0 or position.winner() != None: #at last node of tree OR the game is over
        return position.evaluate(), position #get position & its evaluation
    
    if max_player: #goal = to maximize score
        maxEval = float('-inf')
        best_move = None #stores best move we can make

        for move in get_all_moves(position, "orange", game): #for all moves that can be made we want to evaluate them
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move

    else: #min_player & goal = to minimize score
        minEval = float('inf')
        best_move = None

        for move in get_all_moves(position, "blue", game): 
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move
    

def simulate_move(piece, move, board, game, skip):
    board.move_piece(piece, move[0], move[1])
    if skip:
        board.remove(skip) #skip is the piece to be "removed"

    return board

def get_all_moves(board, color, game):
    #get all possible moves we can make from current position
    moves = [] #blank list of potential new boards and the pieces that caused it

    for piece in board.get_all_pieces(color): #loop through all pieces in board of a certain color
        valid_moves = board.get_valid_moves(piece) #get all valid moves for a certain piece
        for move, skip in valid_moves.items(): 
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)

            new_board = simulate_move(temp_piece, move, temp_board, game, skip) #takes piece, take move we want to make
            moves.append(new_board) #if this piece moves then the newboard will look like this
    return moves
