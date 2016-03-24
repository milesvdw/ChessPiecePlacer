import sys
emptychar = "."
threatened = "T"
king = "K"
knight = "N"
pawn = "P"
queen = "Q"
bishop = "B"
rook = "R"

# check to see if the spot has been taken or threatened
def is_available(space, x, y):
    # if the space is out of bounds, then it's definitely not available
    # also, it should be an emptychar
    return 0 <= x < 8 and 0 <= y < 8 and (board[x][y] == emptychar)

def disturbs_space(space, x, y):
    # the first two checks are to make sure the index is in-bounds. if index out of bounds, just let the caller know
    # that it's not threatening things out of bounds. it's not even really a lie, and simplifies several checks.
    # if it's neither empty, nor threatened, then it is a piece
    return 0 <= x < 8 and 0 <= y < 8 and (board[x][y] != emptychar and board[x][y] != threatened)

# note that we define pawns to be side-agnostic: they can attack one square in any diagonal direction
def place_pawn(board, i, j):
    placed = False
    if is_available(board, i, j):
        available = True
        # ensure that this space doesn't threaten an existing piece,
        # if a location is neither empty, nor threatened, then a piece is in that location
        if disturbs_space(board, i+1, j+1) or \
           disturbs_space(board, i-1, j+1) or \
           disturbs_space(board, i+1, j-1) or \
           disturbs_space(board, i-1, j-1):
            available = False

        # check to see if the spot is available
        if available:
            board[i][j] = "P"
            placed = True
            # mark all threatened spaces
            if is_available(board, i+1, j+1):
                board[i+1][j+1] = "T"
            if is_available(board, i-1, j+1):
                board[i-1][j+1] = "T"
            if is_available(board, i+1, j-1):
                board[i+1][j-1] = "T"
            if is_available(board, i-1, j-1):
                board[i-1][j-1] = "T"
    return placed

def place_king(board, i, j):
    placed = False
    if is_available(board, i, j):
        available = True
        # ensure that this space doesn't threaten an existing piece,
        # if a location is neither empty, nor threatened, then a piece is in that location
        if disturbs_space(board, i+1, j+1) or \
           disturbs_space(board, i-1, j+1) or \
           disturbs_space(board, i+1, j-1) or \
           disturbs_space(board, i-1, j-1) or \
           disturbs_space(board, i, j+1) or \
           disturbs_space(board, i, j-1) or \
           disturbs_space(board, i+1, j) or \
           disturbs_space(board, i-1, j):
            available = False

        # check to see if the spot is available
        if available:
            board[i][j] = "K"
            placed = True
            # mark all threatened spaces
            if is_available(board, i+1, j+1):
                board[i+1][j+1] = "T"
            if is_available(board, i-1, j+1):
                board[i-1][j+1] = "T"
            if is_available(board, i+1, j-1):
                board[i+1][j-1] = "T"
            if is_available(board, i-1, j-1):
                board[i-1][j-1] = "T"
            if is_available(board, i, j+1):
                board[i-1][j-1] = "T"
            if is_available(board, i, j-1):
                board[i-1][j-1] = "T"
            if is_available(board, i+1, j):
                board[i-1][j-1] = "T"
            if is_available(board, i-1, j):
                board[i-1][j-1] = "T"
    return placed

def place_knight(board, i, j):
    placed = False
    if is_available(board, i, j):
        available = True
        # ensure that this space doesn't threaten an existing piece,
        # if a location is neither empty, nor threatened, then a piece is in that location
        if disturbs_space(board, i+2, j+1) or \
           disturbs_space(board, i+2, j-1) or \
           disturbs_space(board, i-2, j+1) or \
           disturbs_space(board, i-2, j-1) or \
           disturbs_space(board, i+1, j+2) or \
           disturbs_space(board, i-1, j+2) or \
           disturbs_space(board, i+1, j-2) or \
           disturbs_space(board, i-1, j-2):
            available = False

        # check to see if the spot is available
        if available:
            board[i][j] = "N"
            placed = True
            # mark all threatened spaces
            if is_available(board, i+2, j+1):
                board[i+2][j+1] = "T"
            if is_available(board, i+2, j-1):
                board[i+2][j-1] = "T"
            if is_available(board, i-2, j+1):
                board[i-2][j+1] = "T"
            if is_available(board, i-2, j-1):
                board[i-2][j-1] = "T"
            if is_available(board, i+1, j+2):
                board[i+1][j+2] = "T"
            if is_available(board, i-1, j+2):
                board[i-1][j+2] = "T"
            if is_available(board, i+1, j-2):
                board[i+1][j-2] = "T"
            if is_available(board, i-1, j-2):
                board[i-1][j-2] = "T"
    return placed

def place_rook(board, i, j):
    placed = False
    # check to see if the spot is used or threatened
    if is_available(board, i, j):
        available = True

        # ensure that this doesn't threaten an already-placed piece:
        for x in range(8):
            # if it's neither empty, nor threatened, then it is a piece
            if disturbs_space(board, i, x) or disturbs_space(board, x, j):
                # can't use this spot!
                available = False
                break

        if available:
            placed = True
            board[i][j] = "R"
            # mark all threatened spaces
            for k in range(8):
                if is_available(board, k, j):
                    board[k][j] = "T"
                if is_available(board, i, k):
                    board[i][k] = "T"
    return placed

def place_bishop(board, i, j):
    placed = False
    # check to see if the spot is used or threatened
    if is_available(board, i, j):
        available = True

        # ensure that this doesn't threaten an already-placed piece:
        for c in range(8):
            # if it's neither empty, nor threatened, then it is a piece
            if disturbs_space(board, i-c, j-c) or \
               disturbs_space(board, i+c, j+c) or \
               disturbs_space(board, i-c, j+c) or \
               disturbs_space(board, i+c, j-c):
                # can't use this spot!
                available = False
                break

        if available:
            placed = True
            board[i][j] = "B"
            # mark all threatened spaces
            for c in range(8):
                # if it's neither empty, nor threatened, then it is a piece
                if is_available(board, i-c, j-c):
                    board[i-c][j-c] = "T"
                if is_available(board, i-c, j+c):
                    board[i-c][j+c] = "T"
                if is_available(board, i+c, j-c):
                    board[i+c][j-c] = "T"
                if is_available(board, i+c, j+c):
                    board[i+c][j+c] = "T"

    return placed

def place_queen(board, i, j):
    placed = False
    # check to see if the spot is used or threatened
    if is_available(board, i, j):
        available = True

        # ensure that this doesn't threaten an already-placed piece:
        for c in range(8):
            # if it's neither empty, nor threatened, then it is a piece
            if disturbs_space(board, i-c, j-c) or \
               disturbs_space(board, i+c, j+c) or \
               disturbs_space(board, i-c, j+c) or \
               disturbs_space(board, i+c, j-c) or \
               disturbs_space(board, i, c) or \
               disturbs_space(board, c, j):
                # can't use this spot!
                available = False
                break

        if available:
            placed = True
            board[i][j] = "Q"
            # mark all threatened spaces
            for c in range(8):
                # if it's neither empty, nor threatened, then it is a piece
                if is_available(board, i-c, j-c):
                    board[i-c][j-c] = "T"
                if is_available(board, i-c, j+c):
                    board[i-c][j+c] = "T"
                if is_available(board, i+c, j-c):
                    board[i+c][j-c] = "T"
                if is_available(board, i+c, j+c):
                    board[i+c][j+c] = "T"
                if is_available(board, c, j):
                    board[c][j] = "T"
                if is_available(board, i, c):
                    board[i][c] = "T"

    return placed

def place_piece(board, piece, x, y):
    if piece == "pawn":
        return place_pawn(board, x, y)
    elif piece == "rook":
        return place_rook(board, x, y)
    elif piece == "bishop":
        return place_bishop(board, x, y)
    elif piece == "knight":
        return place_knight(board, x, y)
    elif piece == "king":
        return place_king(board, x, y)
    elif piece == "queen":
        return place_queen(board, x, y)

# initialize the board with + in each empty space
def init_board(board):
    for i in range(8):
        board.append([])
        for j in range(8):
            board[i].append(emptychar)

def print_board(board):
    for i in range(8):
        print
        for j in range(8):
            if board[i][j] == threatened:
                print emptychar,
            else:
                print board[i][j],

def guess_placement(board, pieces, x, y):
    piece = pieces.pop()
    # base case, try to place the last piece then return
    if len(pieces) == 0:
        return place_piece(board, piece, x, y)
    # otherwise, place the next piece and go back to the setup_board state
    elif place_piece(board, piece, x, y):
        return setup_board(board, pieces)
    else:
        return False

def setup_board(board, pieces):
    for x in range(8):
        for y in range(8):
            copyboard = [list(p) for p in board]
            copypieces = list(pieces)
            # try putting our first piece in this location
            if guess_placement(board, pieces, x, y):
                # success!
                return True
            else:
                # failure! revert the board and try again
                del board[:]
                for p in copyboard:
                    board.append(p)
                # board = [list(p) for p in copyboard]
                del pieces[:]
                for p in copypieces:
                    pieces.append(p)
    return False

if __name__ == "__main__":
    # get the list of space-separated pieces
    pieces = sys.argv[1].split(" ")
    board = []
    init_board(board)

    ret = setup_board(board, pieces)

    print_board(board)
