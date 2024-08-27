"""
1   br   bn   bb   bk   bq   bb   bn   br                1   2   3   4   5   6   7   8
2   bp   bp   bp   bp   bp   bp   bp   bp                9  10  11  12  13  14  15  16
3   0    0    0    0    0    0    0    0                17  18  19  20  21  22  23  24
4   0    0    0    0    0    0    0    0                25  26  27  28  29  30  31  32
5   0    0    0    0    0    0    0    0                33  34  35  36  37  38  39  40
6   0    0    0    0    0    0    0    0                41  42  43  44  45  46  47  48
7   wp   wp   wp   wp   wp   wp   wp   wp               49  50  51  52  53  54  55  56
8   wr   wn   wb   wk   wq   wb   wn   wr               57  58  59  60  61  62  63  64
    A    B    C    D    E    F    G    H

1. Create array representing chess board
2. Define game rules and turns
3. Define function to check chess board and piece
4. Define different movement functions
5. Give pieces and coordinates weight
6. Create algorythm for move evaluation by calculating shifts in weight from own move and responses from opponent
7. Improvements: checks and pressuring moves for tempo, stalemate forcing in losing positions, take out pieces from dict
   that are not on the field anymore
"""
import random

# ------------------------------------------ Variables ------------------------------------------------------------

empty_square = 0
w_piece_dict = {1: 'w_pawn', 2: 'w_rook', 3: 'w_knight', 4: 'w_bishop', 5: 'w_queen', 6: 'w_king'}
b_piece_dict = {7: 'b_pawn', 8: 'b_rook', 9: 'b_knight', 10: 'b_bishop', 11: 'b_queen', 12: 'b_king'}
white_legal_moves = []
black_legal_moves = []

# ------------------------------------------ 1. Create array representing chess board --------------------------------

chess_board = [[0, 0, 0, 0, 12, 0, 0, 0],
               [0, 0, 1, 1, 7, 0, 0, 0],
               [0, 0, 1, 10, 7, 0, 0, 0],
               [0, 0, 7, 1, 7, 0, 0, 0],
               [7, 10, 0, 0, 0, 0, 0, 0],
               [0, 7, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 1, 1, 1, 1, 1],
               [0, 3, 4, 0, 6, 4, 3, 2]]
'''chess_board = [[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 8, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 8, 0],
               [8, 0, 0, 0, 8, 0, 0, 0],
               [0, 1, 0, 1, 0, 1, 0, 1],
               [0, 0, 0, 0, 0, 0, 0, 0]]'''

x = 0
y = 0
new_x = 0
new_y = 0
w_king_pos = None
b_king_pos = None

# ----------------------------------------- 2. Define game rules and turns --------------------------------
is_white_turn = True
current_piece_pos = [None]


def iterate_white_pieces(chess_board):
    global current_piece_pos
    global white_legal_moves
    for x in range(8):
        for y in range(8):
            piece = chess_board[x][y]
            if 0 < piece < 7:
                print(w_piece_dict.get(piece))
                get_white_legal_moves(w_piece_dict.get(piece), x, y)
                print(white_legal_moves)
                if white_legal_moves:
                    current_piece_pos = (x, y)
# function to iterate the white pieces from the chess board
    # iterate over chess board
        # get piece_value, which is the value of the iterated piece
        # if value is > 0 and < 7
            # then get x and y
            # get_white_legal_moves(w_piece_dict[piece_value], x, y)


def iterate_black_pieces(chess_board):
    global current_piece_pos
    global black_legal_moves
    for x in range(8):
        for y in range(8):
            piece = chess_board[x][y]
            if 6 < piece < 13:
                print(b_piece_dict.get(piece))
                get_black_legal_moves(b_piece_dict.get(piece), x, y)
                print(black_legal_moves)
                if black_legal_moves:
                    current_piece_pos = (x, y)


def execute_white_move(piece, x, y, new_x, new_y):
    global white_legal_moves
    global current_piece_pos
    iterate_white_pieces(chess_board)
    if not white_legal_moves:
        print("no legal moves allowed for white")
        return
    for move in white_legal_moves:
        if len(move) == 4:
            print(f"Move from ({move[0]}, {move[1]} to {move[2]}, {move[3]})")
        else:
            print(f"Move to ({move[0]}, {move[1]})")
    white_choice = random.choice(white_legal_moves)
    print('random move =', white_choice)
    new_x, new_y = white_choice
    update_chess_board(chess_board, current_piece_pos[0], current_piece_pos[1], new_x, new_y)
    white_legal_moves = []


def execute_black_move(piece, x, y, new_x, new_y):
    global black_legal_moves
    global current_piece_pos
    iterate_black_pieces(chess_board)
    if not black_legal_moves:
        print("no legal moves allowed for black")
        return
    for move in black_legal_moves:
        if len(move) == 4:
            print(f"Move from ({move[0]}, {move[1]} to {move[2]}, {move[3]})")
        else:
            print(f"Move to ({move[0]}, {move[1]})")
    black_choice = random.choice(black_legal_moves)
    print('random move =', black_choice)
    new_x, new_y = black_choice
    update_chess_board(chess_board, current_piece_pos[0], current_piece_pos[1], new_x, new_y)
    black_legal_moves = []


def changing_turns(x, y, new_x, new_y):
    global is_white_turn
    piece = chess_board[x][y]

    while is_white_turn:
        print("white moves")
        execute_white_move(piece, x, y, new_x, new_y)
        if is_king_in_check(chess_board, True):
            if is_check_mate(chess_board, True):
                print("Checkmate for Black")
                return
            print("White is in check")

        is_white_turn = False
    else:
        print("black moves")
        execute_black_move(piece, x, y, new_x, new_y)
        if is_king_in_check(chess_board, True):
            if is_check_mate(chess_board, True):
                print("Checkmate for White")
                return
            print("Black is in check")
        is_white_turn = True


def print_updated_chess_board(chess_board):
    piece_symbols = {
        0: '0', 1: 'P', 2: 'R', 3: 'N', 4: 'B', 5: 'Q', 6: 'K',
        7: 'p', 8: 'r', 9: 'n', 10: 'b', 11: 'q', 12: 'k'
    }
    print("Current Chess Board:")
    for row in chess_board:
        print(" ".join(piece_symbols.get(piece, str(piece)) for piece in row))
    print("\n")


def update_chess_board(chess_board, x, y, new_x, new_y):
    global w_king_pos, b_king_pos
    piece = chess_board[x][y]

    # updating the chessboard
    chess_board[new_x][new_y] = piece
    chess_board[x][y] = 0

    # updating the king positions in case they were moved
    if piece == 6:     # (white king)
        w_king_pos = (new_x, new_y)
    elif piece == 12:   # (black king)
        b_king_pos = (new_x, new_y)

    print_updated_chess_board(chess_board)


# ------------------------------------- 3. Define function to check chess board and piece -----------------------

def generate_opponents_moves(chess_board, is_white_turn):
    legal_moves = []    # list for moves

    for x in range(8):
        for y in range(8):
            piece = chess_board[x][y]
            if (is_white_turn and 0 < piece < 7) or (not is_white_turn and 6 < piece < 13):
                get_white_legal_moves(w_piece_dict.get(piece), x, y) if is_white_turn else \
                get_black_legal_moves(b_piece_dict.get(piece), x, y)
                legal_moves.extend(white_legal_moves if is_white_turn else black_legal_moves)
    return legal_moves


def is_king_in_check(chess_board, is_white_turn):
    king_pos = w_king_pos if is_white_turn else b_king_pos
    opponents_moves = generate_opponents_moves(chess_board, not is_white_turn)

    return king_pos in opponents_moves


def is_check_mate(chess_board, is_white_turn):
    if not is_king_in_check(chess_board, is_white_turn):
        return False

    for x in range(8):
        for y in range(8):
            piece = chess_board
            if (is_white_turn and 0 < piece < 7) or (not is_white_turn and 6 < piece < 13):
                legal_moves = white_legal_moves if is_white_turn else black_legal_moves
                for move in legal_moves:
                    temp_board = [row[:] for row in chess_board]
                    update_chess_board(temp_board, x, y, move[0], move[1])
                    if not is_king_in_check(temp_board, is_white_turn):
                        return False
    return True


def get_white_legal_moves(piece, x, y):
    global white_legal_moves
    white_legal_moves = []
    if piece == 'w_pawn':
        white_pawn_movement(chess_board, x, y)
    elif piece == 'w_knight':
        white_knight_movement(x, y)
    elif piece == 'w_rook':
        white_horizontal_movement(x, y)
        white_vertical_movement(x, y)
    elif piece == 'w_bishop':
        white_diagonal_movement(x, y)
    elif piece == 'w_queen':
        white_horizontal_movement(x, y)
        white_vertical_movement(x, y)
        white_diagonal_movement(x, y)
    elif piece == 'w_king':
        white_king_movement(x, y)


def get_black_legal_moves(piece, x, y):
    global black_legal_moves
    black_legal_moves = []
    if piece == 'b_pawn':
        black_pawn_movement(x, y)
    elif piece == 'b_knight':
        black_knight_movement(x, y)
    elif piece == 'b_rook':
        black_horizontal_movement(x, y)
        black_vertical_movement(x, y)
    elif piece == 'b_bishop':
        black_diagonal_movement(x, y)
    elif piece == 'b_queen':
        black_horizontal_movement(x, y)
        black_vertical_movement(x, y)
        black_diagonal_movement(x, y)
    elif piece == 'b_king':
        black_king_movement(x, y)

# to run the functions for getting legal moves

# ---------------------------------- 4. Define different movement functions ------------------------------


def white_pawn_movement(chess_board, x, y):
    if x > 0:
        # moving forward if space ahead is empty
        if chess_board[x - 1][y] == 0:
            white_legal_moves.append([x - 1, y])
        # moving forward 2 spaces if in original position and both are empty
        if x == 6 and chess_board[x - 1][y] == 0 and chess_board[x - 2][y] == 0:
            white_legal_moves.append([x - 2, y])
        # capturing the piece diagonally right
        if y < 7 and 6 < chess_board[x - 1][y + 1] < 13:
            white_legal_moves.append([x - 1, y + 1])
        # Capturing the piece diagonally left
        if y > 0 and 6 < chess_board[x - 1][y - 1] < 13:
            white_legal_moves.append([x - 1, y - 1])


def black_pawn_movement(x, y):
    if x > 0:
        # moving forward if space ahead is empty
        if chess_board[x + 1][y] == 0:
            black_legal_moves.append([x + 1, y])
        # moving forward 2 spaces if in original position and both are empty
        if x == 6 and chess_board[x + 1][y] == 0 and chess_board[x + 2][y] == 0:
            black_legal_moves.append([x + 2, y])
        # capturing the piece diagonally right
        if y < 7 and 0 < chess_board[x + 1][y + 1] < 7:
            black_legal_moves.append([x + 1, y + 1])
        # Capturing the piece diagonally left
        if y > 0 and 0 < chess_board[x + 1][y - 1] < 7:
            black_legal_moves.append([x + 1, y - 1])


def white_knight_movement(x, y):
    knight_moves = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1))
    for (j, k) in knight_moves:
        if 7 >= x + j >= 0 and 7 >= y + k >= 0:
            if chess_board[x + j][y + k] == 0:
                white_legal_moves.append([x + j, y + k])
            elif 6 < chess_board[x + j][y + k] < 13:
                white_legal_moves.append([x + j, y + k])


def black_knight_movement(x, y):
    knight_moves = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1))
    for (j, k) in knight_moves:
        if 7 >= x + j >= 0 and 7 >= y + k >= 0:
            if chess_board[x + j][y + k] == 0:
                black_legal_moves.append([x + j, y + k])
            elif 0 < chess_board[x + j][y + k] < 7:
                black_legal_moves.append([x + j, y + k])


def white_horizontal_movement(x, y):
    # horizontal movement to the right:
    for j in range(1, 8 - y):
        new_y = y + j
        if 0 <= new_y < 8:
            # checking for empty squares:
            if chess_board[x][new_y] == 0:
                white_legal_moves.append([x, new_y])
            # checking for squares with opposing pieces:
            elif 6 < chess_board[x][new_y] < 13:
                white_legal_moves.append([x, new_y])
                break
            # breaking the function when the only option is for a friendly piece to be ahead
            else:
                break

    # horizontal movement to the left:
    for k in range(1, y + 1):
        new_y = y - k
        if 0 <= new_y < 8:
            if chess_board[x][new_y] == 0:
                white_legal_moves.append([x, new_y])
            elif 6 < chess_board[x][new_y] < 13:
                white_legal_moves.append([x, new_y])
                break
            else:
                break


def black_horizontal_movement(x, y):
    # horizontal movement to the right:
    for j in range(1, 8 - y):
        new_y = y + j
        if 0 <= new_y < 8:
            # checking for empty squares:
            if chess_board[x][new_y] == 0:
                black_legal_moves.append([x,new_y])
            # checking for squares with opposing pieces:
            elif 0 < chess_board[x][new_y] < 7:
                black_legal_moves.append([x, new_y])
                break
            # breaking the function when the only option is for a friendly piece to be ahead
            else:
                break

    # horizontal movement to the left:
    for k in range(1, y + 1):
        new_y = y - k
        if 0 <= new_y < 8:
            if chess_board[x][new_y] == 0:
                black_legal_moves.append([x, new_y])
            elif 0 < chess_board[x][new_y] < 7:
                black_legal_moves.append([x, new_y])
                break
            else:
                break


def white_vertical_movement(x, y):
    for j in range(1, 8 - x):
        new_x = x + j
        if 0 <= new_y < 8:
            if chess_board[new_x][y] == 0:
                white_legal_moves.append([new_x, y])
            elif 6 < chess_board[new_x][y] < 13:
                white_legal_moves.append([new_x, y])
                break
            else:
                break
    for k in range(1, x + 1):
        new_x = x - k
        if 0 <= new_y < 8:
            if chess_board[new_x][y] == 0:
                white_legal_moves.append([new_x, y])
            elif 6 < chess_board[new_x][y] < 13:
                white_legal_moves.append([new_x, y])
                break
            else:
                break
# vertical movement function for white queen, rook


def black_vertical_movement(x, y):
    for j in range(1, 8 - x):
        new_x = x + j
        if 0 <= new_y < 8:
            if chess_board[new_x][y] == 0:
                black_legal_moves.append([new_x, y])
            elif 0 < chess_board[new_x][y] < 7:
                black_legal_moves.append([new_x, y])
                break
            else:
                break
    for k in range(1, x + 1):
        new_x = x - k
        if 0 <= new_y < 8:
            if chess_board[new_x][y] == 0:
                black_legal_moves.append([new_x, y])
            elif 0 < chess_board[new_x][y] < 7:
                black_legal_moves.append([new_x, y])
                break
            else:
                break
# vertical movement function for black queen, rook


def white_diagonal_movement(x, y):
    # diagonal movement to the top left(-x, -y)
    for j in range(1, 8):
        new_x, new_y = x - j, y - j
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                white_legal_moves.append([new_x, new_y])
            elif 6 < chess_board[new_x][new_y] < 13:
                white_legal_moves.append([new_x, new_y])
                break
            else:
                break
    # diagonal movement to the top right(-x, +y)
    for k in range(1, 8):
        new_x, new_y = x - k, y + k
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                white_legal_moves.append([new_x, new_y])
            elif 6 < chess_board[new_x][new_y] < 13:
                white_legal_moves.append([new_x, new_y])
                break
            else:
                break
    # diagonal movement to the bottom right( +x, +y)
    for m in range(1, 8):
        new_x, new_y = x + m, y + m
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                white_legal_moves.append([new_x, new_y])
            elif 6 < chess_board[new_x][new_y] < 13:
                white_legal_moves.append([new_x, new_y])
                break
            else:
                break
    # diagonal movement to the bottom left( +x, -y)
    for n in range(1, 8):
        new_x, new_y = x + n, y - n
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                white_legal_moves.append([new_x, new_y])
            elif 6 < chess_board[new_x][new_y] < 13:
                white_legal_moves.append([new_x, new_y])
                break
            else:
                break


def black_diagonal_movement(x, y):
    # diagonal movement to the top left(-x, -y)
    for j in range(1, 8):
        new_x, new_y = x - j, y - j     # moving x up and y left
        if 0 <= new_x < 8 and 0 <= new_y < 8:       # checking that x and y are within the chessboard
            # print(f"Checking position: {new_x}, {new_y} -> {chess_board[new_x][new_y]}")
            if chess_board[new_x][new_y] == 0:      # checking for an empty square
                black_legal_moves.append([new_x, new_y])
                # print(f"Empty square: {new_x}, {new_y} -> {chess_board[new_x][new_y]}")
            elif 0 < chess_board[new_x][new_y] < 7:        # checking for a white piece to take
                black_legal_moves.append([new_x, new_y])
                # print(f"Captured at: {new_x}, {new_y}")
                break        # breaking after taking the piece
            else:       # last possibility is a friendly piece, so the function breaks
                # print(f"Friendly piece at: {new_x}, {new_y}")
                break
    # diagonal movement to the top right(-x, +y)
    for k in range(1, 8):
        new_x, new_y = x - k, y + k
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                black_legal_moves.append([new_x, new_y])
            elif 0 < chess_board[new_x][new_y] < 7:
                black_legal_moves.append([new_x, new_y])
                break
            else:
                break
    # diagonal movement to the bottom right( +x, +y)
    for m in range(1, 8):
        new_x, new_y = x + m, y + m
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                black_legal_moves.append([new_x, new_y])
            elif 0 < chess_board[new_x][new_y] < 7:
                black_legal_moves.append([new_x, new_y])
                break
            else:
                break
    # diagonal movement to the bottom left( +x, -y)
    for n in range(1, 8):
        new_x, new_y = x + n, y - n
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                black_legal_moves.append([new_x, new_y])
            elif 0 < chess_board[new_x][new_y] < 7:
                black_legal_moves.append([new_x, new_y])
                break
            else:
                break


def white_king_movement(x, y):
    king_moves = ((1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1))
    for (j, k) in king_moves:
        if 7 >= x + j >= 0 and 7 >= y + k >= 0:
            if not 0 < chess_board[x + j][y + k] < 7:
                white_legal_moves.append([x + j, y + k])
# movement function for white king


def black_king_movement(x, y):
    king_moves = ((1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1))
    for (j, k) in king_moves:
        if 7 >= x + j >= 0 and 7 >= y + k >= 0:
            if not 6 < chess_board[x + j][y + k] < 13:
                black_legal_moves.append([x + j, y + k])
# movement function for black king


if __name__ == '__main__':
    for i in range(8):
        print(chess_board[i])
    for j in range(1):
        changing_turns(x, y, new_x, new_y)
    # get_legal_moves(piece, x, y)
    # black_horizontal_movement(x, y)
    # white_horizontal_movement(x, y)
    # white_vertical_movement(x, y)
    # black_vertical_movement(x, y)
    # white_diagonal_movement(x, y)
    # black_diagonal_movement(x, y)
    # white_pawn_movement(x, y)
    # black_pawn_movement(x, y)
    # white_knight_movement(x, y)
    # black_knight_movement(x, y)
    # white_king_movement(x, y)
    # black_king_movement(x, y)
    print(white_legal_moves)
