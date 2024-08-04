"""
1   br   bh   bb   bk   bq   bb   bh   br                1   2   3   4   5   6   7   8
2   bp   bp   bp   bp   bp   bp   bp   bp                9  10  11  12  13  14  15  16
3   0    0    0    0    0    0    0    0                17  18  19  20  21  22  23  24
4   0    0    0    0    0    0    0    0                25  26  27  28  29  30  31  32
5   0    0    0    0    0    0    0    0                33  34  35  36  37  38  39  40
6   0    0    0    0    0    0    0    0                41  42  43  44  45  46  47  48
7   wp   wp   wp   wp   wp   wp   wp   wp               49  50  51  52  53  54  55  56
8   wr   wh   wb   wk   wq   wb   wh   wr               57  58  59  60  61  62  63  64
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
w_piece_dict = {'w_pawn': 1, 'w_rook': 2, 'w_knight': 3, 'w_bishop': 4, 'w_queen': 5, 'w_king': 6}
b_piece_dict = {'b_pawn': 7, 'b_rook': 8, 'b_knight': 9, 'b_bishop': 10, 'b_queen': 11, 'b_king': 12}
white_legal_moves = []
black_legal_moves = []
x = 4
y = 4
# ------------------------------------------ 1. Create array representing chess board --------------------------------

chess_board = [[8, 9, 10, 11, 12, 10, 9, 8],
               [7, 7, 7, 7, 7, 7, 7, 7],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 8, 0, 0, 5, 0, 8, 0],
               [1, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [2, 3, 4, 5, 6, 4, 3, 2]]

# ----------------------------------------- 2. Define game rules and turns --------------------------------
is_white_turn = True


def white_move_piece(x_pos, y_pos, white_choice, piece_name):
    chess_board[x][y] = 0
    x_final_pos = white_choice[0]
    y_final_pos = white_choice[0]
    chess_board[x_final_pos][y_final_pos] = w_piece_dict.get(piece_name)


def black_move_piece(x_pos, y_pos, black_choice, piece_name):
    chess_board[x][y] = 0
    x_final_pos = black_choice[0]
    y_final_pos = black_choice[1]
    chess_board[x_final_pos][y_final_pos] = b_piece_dict.get(piece_name)


def white_move(piece_name):
    white_choice = random.choice(white_legal_moves)
    print('random move =', white_choice)
    white_move_piece(x, y, white_choice, piece_name)


def black_move(piece_name):
    black_choice = random.choice(black_legal_moves)
    black_move_piece(x, y, black_choice, piece_name)


def turn_order(piece_name):
    global is_white_turn
    if is_white_turn:
        print("white moves")
        white_move(piece_name)
        is_white_turn = False
    else:
        print("black moves")
        black_move(piece_name)
        is_white_turn = True


# ------------------------------------- 3. Define function to check chess board and piece -----------------------


def get_legal_moves(piece_name):
    if piece_name == 'w_pawn':
        white_pawn_movement(x, y)
    if piece_name == 'b_pawn':
        black_pawn_movement(x, y)
    if piece_name == 'w_knight':
        white_knight_movement(x, y)
    if piece_name == 'b_knight':
        black_knight_movement(x, y)
    if piece_name == 'w_rook':
        white_horizontal_movement(x, y)
        white_vertical_movement(x, y)
    if piece_name == 'b_rook':
        black_horizontal_movement(x, y)
        black_vertical_movement(x, y)
    if piece_name == 'w_bishop':
        white_diagonal_movement(x, y)
    if piece_name == 'b_bishop':
        black_diagonal_movement(x, y)
    if piece_name == 'w_queen':
        white_horizontal_movement(x, y)
        white_vertical_movement(x, y)
        white_diagonal_movement(x, y)
    if piece_name == 'b_queen':
        black_horizontal_movement(x, y)
        black_vertical_movement(x, y)
        black_diagonal_movement(x, y)
    if piece_name == 'w_king':
        white_king_movement(x, y)
    if piece_name == 'b_king':
        black_king_movement(x, y)
# to run the functions for getting legal moves

# ---------------------------------- 4. Define different movement functions ------------------------------


def white_pawn_movement(x_pos, y_pos):
    if chess_board[x - 1][y] == 0:
        white_legal_moves.append([x - 1, y])
    if chess_board[4][y] == 0 and chess_board[5][y] == 0:
        white_legal_moves.append([x - 2, y])
    if chess_board[x - 1][y + 1] in b_piece_dict.values():
        white_legal_moves.append([x - 1, y + 1])
        # print('result', [x - 1, y + 1])
    if chess_board[x - 1][y - 1] in b_piece_dict.values():
        white_legal_moves.append([x - 1, y - 1])
# movement function for white pawn


def black_pawn_movement(x_pos, y_pos):
    if chess_board[x + 1][y] == 0:
        black_legal_moves.append([x + 1, y])
    if chess_board[4][y] == 0 and chess_board[5][y] == 0:
        black_legal_moves.append([x + 2, y])
    if chess_board[x + 1][y + 1] in w_piece_dict.values():
        black_legal_moves.append([x + 1, y + 1])
    if chess_board[x + 1][y - 1] in w_piece_dict.values():
        black_legal_moves.append([x + 1, y - 1])
# movement function for black pawn


def white_knight_movement(x_pos, y_pos):
    knight_moves = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1))
    for (j, k) in knight_moves:
        if 7 >= x + j >= 0 and 7 >= y + k >= 0:
            if chess_board[x + j][y + k] not in w_piece_dict.values():
                white_legal_moves.append([x + j, y + k])


# movement function for white knight


def black_knight_movement(x_pos, y_pos):
    knight_moves = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1))
    for (j, k) in knight_moves:
        if 7 >= x + j >= 0 and 7 >= y + k >= 0:
            if chess_board[x + j][y + k] not in b_piece_dict.values():
                black_legal_moves.append([x + j, y + k])
# movement function for black knight


def white_horizontal_movement(x_pos, y_pos):
    for j in range(y):
        if chess_board[x][y - j - 1] == 0:
            white_legal_moves.append([x, y - j - 1])
        if chess_board[x][y - j - 1] in w_piece_dict.values():
            break
        if chess_board[x][y - j - 1] in b_piece_dict.values():
            white_legal_moves.append([x, y - j - 1])
            break
    for k in range(7 - y):
        if chess_board[x][y + k + 1] == 0:
            white_legal_moves.append([x, y + k + 1])
        if chess_board[x][y + k + 1] in w_piece_dict.values():
            break
        if chess_board[x][y + k + 1] in b_piece_dict.values():
            white_legal_moves.append([x, y + k + 1])
            break
# horizontal movement function for white queen, rook


def black_horizontal_movement(x_pos, y_pos):
    for j in range(y):
        if chess_board[x][y - j - 1] == 0:
            black_legal_moves.append([x, y - j - 1])
        if chess_board[x][y - j - 1] in b_piece_dict.values():
            break
        if chess_board[x][y - j - 1] in w_piece_dict.values():
            black_legal_moves.append([x, y - j - 1])
            break
    for k in range(7 - y):
        if chess_board[x][y + k + 1] == 0:
            black_legal_moves.append([x, y + k + 1])
        if chess_board[x][y + k + 1] in b_piece_dict.values():
            break
        if chess_board[x][y + k + 1] in w_piece_dict.values():
            black_legal_moves.append([x, y + k + 1])
            break
# horizontal movement function for black queen, rook


def white_vertical_movement(x_pos, y_pos):
    for j in range(x):
        if chess_board[x - j - 1][y] == 0:
            white_legal_moves.append([x - j - 1, y])
        if chess_board[x - j - 1][y] in w_piece_dict.values():
            break
        if chess_board[x - j - 1][y] in b_piece_dict.values():
            white_legal_moves.append([x - j - 1, y])
            break
    for k in range(7 - x):
        if chess_board[x + k + 1][y] == 0:
            white_legal_moves.append([x + k + 1, y])
        if chess_board[x + k + 1][y] in w_piece_dict.values():
            break
        if chess_board[x + k + 1][y] in b_piece_dict.values():
            white_legal_moves.append([x + k + 1, y])
            break
# vertical movement function for white queen, rook


def black_vertical_movement(x_pos, y_pos):
    for j in range(x):
        if chess_board[x - j - 1][y] == 0:
            black_legal_moves.append([x - j - 1, y])
        if chess_board[x - j - 1][y] in b_piece_dict.values():
            break
        if chess_board[x - j - 1][y] in w_piece_dict.values():
            black_legal_moves.append([x - j - 1, y])
            break
    for k in range(7 - x):
        if chess_board[x + k + 1][y] == 0:
            black_legal_moves.append([x + k + 1, y])
        if chess_board[x + k + 1][y] in b_piece_dict.values():
            break
        if chess_board[x + k + 1][y] in w_piece_dict.values():
            black_legal_moves.append([x + k + 1, y])
            break
# vertical movement function for black queen, rook


def white_diagonal_movement(x_pos, y_pos):
    for j in range(7):
        if chess_board[x - j - 1][y - j - 1] == 0:
            white_legal_moves.append([x - j - 1, y - j - 1])
        if chess_board[x - j - 1][y - j - 1] in w_piece_dict.values():
            break
        if chess_board[x - j - 1][y - j - 1] in b_piece_dict.values():
            white_legal_moves.append([x - j - 1, y - j - 1])
            break
    for k in range(7):
        if chess_board[x + k + 1][y - k - 1] == 0:
            white_legal_moves.append([x + k + 1, y - k - 1])
        if chess_board[x + k + 1][y - k - 1] in w_piece_dict.values():
            break
        if chess_board[x + k + 1][y - k - 1] in b_piece_dict.values():
            white_legal_moves.append([x + k + 1, y - k - 1])
            break
    for m in range(7):
        if chess_board[x + m + 1][y + m + 1] == 0:
            white_legal_moves.append([x + m + 1, y + m + 1])
        if chess_board[x + m + 1][y + m + 1] in w_piece_dict.values():
            break
        if chess_board[x + m + 1][y + m + 1] in b_piece_dict.values():
            white_legal_moves.append([x + m + 1, y + m + 1])
            break
    for n in range(7):
        if chess_board[x - n - 1][y + n + 1] == 0:
            white_legal_moves.append([x - n - 1, y + n + 1])
        if chess_board[x - n - 1][y + n + 1] in w_piece_dict.values():
            break
        if chess_board[x - n - 1][y + n + 1] in b_piece_dict.values():
            white_legal_moves.append([x - n - 1, y + n + 1])
            break
# diagonal movement function for white queen, bishop


def black_diagonal_movement(x_pos, y_pos):
    for j in range(7):
        if chess_board[x - j - 1][y - j - 1] == 0:
            black_legal_moves.append([x - j - 1, y - j - 1])
        if chess_board[x - j - 1][y - j - 1] in b_piece_dict.values():
            break
        if chess_board[x - j - 1][y - j - 1] in w_piece_dict.values():
            black_legal_moves.append([x - j - 1, y - j - 1])
            break
    for k in range(7):
        if chess_board[x + k + 1][y - k - 1] == 0:
            black_legal_moves.append([x + k + 1, y - k - 1])
        if chess_board[x + k + 1][y - k - 1] in b_piece_dict.values():
            break
        if chess_board[x + k + 1][y - k - 1] in w_piece_dict.values():
            black_legal_moves.append([x + k + 1, y - k - 1])
            break
    for m in range(7):
        if chess_board[x + m + 1][y + m + 1] == 0:
            black_legal_moves.append([x + m + 1, y + m + 1])
        if chess_board[x + m + 1][y + m + 1] in b_piece_dict.values():
            break
        if chess_board[x + m + 1][y + m + 1] in w_piece_dict.values():
            black_legal_moves.append([x + m + 1, y + m + 1])
            break
    for n in range(7):
        if chess_board[x - n - 1][y + n + 1] == 0:
            black_legal_moves.append([x - n - 1, y + n + 1])
        if chess_board[x - n - 1][y + n + 1] in b_piece_dict.values():
            break
        if chess_board[x - n - 1][y + n + 1] in w_piece_dict.values():
            black_legal_moves.append([x - n - 1, y + n + 1])
            break
# diagonal movement function for black queen, bishop


def white_king_movement(x_pos, y_pos):
    king_moves = ((1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1))
    for (j, k) in king_moves:
        if 7 >= x + j >= 0 and 7 >= y + k >= 0:
            if chess_board[x + j][y + k] not in w_piece_dict.values():
                white_legal_moves.append([x + j, y + k])
# movement function for white king


def black_king_movement(x_pos, y_pos):
    king_moves = ((1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1))
    for (j, k) in king_moves:
        if 7 >= x + j >= 0 and 7 >= y + k >= 0:
            if chess_board[x + j][y + k] not in b_piece_dict.values():
                black_legal_moves.append([x + j, y + k])
# movement function for black king


if __name__ == '__main__':
    for i in range(8):
        print(chess_board[i])

    piece_name = 'w_queen'
    get_legal_moves(piece_name)
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
    turn_order(piece_name)
