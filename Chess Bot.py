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

#      TODO:
#       - use pygame to implement visual representation of the chessboard *
#       - add a timer to see how long the program needs to make a move
#       - add en passant
#       - fix castling bug *
#       - only allow pieces with legal moves to move, highlight legal moves
#       - improve UI to only allow legal moves to be considered inputs
#       - add promotion rule to pawns *
#       - run tests to check for edge cases and make sure the logic is correct *
#       - start working on move evaluation algorythm:
#           1. minimax system *
#           2. weights for pieces *
#           3. "heatmap" masks for each individual piece *
#           4. implement checkmate into evaluation          // Prio
#           5. tempo/ zugzwang weighing
#           6. moving a piece should make consecutive moves with the same piece weigh less
#           7. friendly pieces defending each other/ attacking same enemy position weigh more   // Prio
#           8. pins on heavy pieces good
#           9. trade pieces when ahead to simplify position
#          10. calculate checks deeper into possible checkmates         // Prio
#       - ideas to make calculation more efficient:
#           1. alpha beta pruning *
#           3. prioritize checks/heavy pieces/positions on the board
#           4. procedural weight map changes according to turn count
#           5. board hashing to prevent simulation for same board outcomes
#           6. magic bit board?


import pygame
import random

from pygame import MOUSEBUTTONUP

empty_square = 0
w_piece_dict = {1: 'w_pawn', 2: 'w_rook', 3: 'w_knight', 4: 'w_bishop', 5: 'w_queen', 6: 'w_king'}
b_piece_dict = {7: 'b_pawn', 8: 'b_rook', 9: 'b_knight', 10: 'b_bishop', 11: 'b_queen', 12: 'b_king'}
w_king_pos = [7, 4]
b_king_pos = [0, 4]
w_king_not_moved = True
b_king_not_moved = True
w_h_rook_not_moved = True
w_a_rook_not_moved = True
b_h_rook_not_moved = True
b_a_rook_not_moved = True
is_white_turn = True

# ------------------------------------------ 1. Create array representing chess board --------------------------------

"""chess_board = [[8, 9, 10, 11, 12, 10, 9, 8],
               [7, 7, 7, 7, 7, 7, 7, 7],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [2, 3, 4, 5, 6, 4, 3, 2]]"""
chess_board = [[0, 0, 0, 0, 12, 0, 0, 8],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 8, 8, 0, 8],
               [0, 0, 0, 0, 0, 6, 0, 0]]

# ------------------------------------------ Pygame Chessboard -------------------------------------------------------

images = {}

pieces = ['w_pawn', 'w_knight', 'w_rook', 'w_bishop', 'w_queen', 'w_king',
          'b_pawn', 'b_knight', 'b_rook', 'b_bishop', 'b_queen', 'b_king']
for piece in pieces:
    images[piece] = pygame.image.load("chess pieces/" + piece + ".png")


def visualize_game_state(screen):
    draw_board(screen)
    draw_pieces(screen, images, chess_board)


def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]

    for row in range(dimensions):
        for column in range(dimensions):
            color = colors[((row + column) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(column * square, row * square, square, square))


def draw_pieces(screen, images, chess_board):
    for row in range(dimensions):
        for column in range(dimensions):
            piece = chess_board[column][row]
            if 0 < piece < 7:
                piece_int = chess_board[column][row]
                piece_str = w_piece_dict.get(piece_int)
                scaled_image = pygame.transform.scale(images[piece_str], (square - 5, square - 5))
                screen.blit(scaled_image, pygame.Rect(row * square, column * square, square, square))
            if 6 < piece < 13:
                piece_int = chess_board[column][row]
                piece_str = b_piece_dict.get(piece_int)
                scaled_image = pygame.transform.scale(images[piece_str], (square - 5, square - 5))
                screen.blit(scaled_image, pygame.Rect(row * square, column * square, square, square))


def get_square_under_mouse(pos):
    x, y = pos
    row = y // square_size
    col = x // square_size
    return (row, col)


# ----------------------------------------- 2. Define game rules and turns --------------------------------

def changing_turns():
    global is_white_turn

    if is_white_turn:
        is_white_turn = False
    else:
        is_white_turn = True


def generate_opponents_moves(chess_board, is_white_turn):
    if is_white_turn:
        legal_moves = [t for xs in get_black_possible_moves(chess_board) for t in xs]
    else:
        legal_moves = [t for xs in get_white_possible_moves(chess_board) for t in xs]
    return legal_moves


def is_king_in_check(temp_board, is_white_turn):
    king_pos = None

    for x in range(len(temp_board)):
        for y in range(len(temp_board[x])):
            if is_white_turn and temp_board[x][y] == 6:
                king_pos = [x, y]
            elif not is_white_turn and temp_board[x][y] == 12:
                king_pos = [x, y]

    for move in generate_opponents_moves(temp_board, is_white_turn):
        if [move[2], move[3]] == king_pos:
            return True

    return False


def is_check_mate(chess_board, is_white_turn):
    if is_white_turn:
        if not get_white_legal_moves(chess_board):
            if is_king_in_check(chess_board, is_white_turn):
                return 'Checkmate'
            else:
                return 'Stalemate'

    else:
        if not get_black_legal_moves(chess_board):
            if is_king_in_check(chess_board, is_white_turn):
                return 'Checkmate'
            else:
                return 'Stalemate'


def simulate_move(chess_board, move):
    # Create a deep copy of the board
    temp_board = [row[:] for row in chess_board]

    # Simulate the move on the temporary board
    piece = temp_board[move[0]][move[1]]
    temp_board[move[2]][move[3]] = piece
    temp_board[move[0]][move[1]] = 0
    # for i in range(8):
    # print("+++", temp_board[i])
    return temp_board


def is_move_legal(chess_board, move, is_white_turn):
    temp_board = simulate_move(chess_board, move)
    # Check if king is in check after the move
    if is_king_in_check(temp_board, is_white_turn):
        return False

    return True


def pawn_promotion(is_white_turn):
    if is_white_turn:
        promoted_piece = 5
    else:
        promoted_piece = 11

    return promoted_piece


def update_chess_board(chess_board, move, is_white_turn):
    global w_king_pos, b_king_pos
    global w_king_not_moved, b_king_not_moved
    global w_h_rook_not_moved, w_a_rook_not_moved, b_h_rook_not_moved, b_a_rook_not_moved
    piece = chess_board[move[0]][move[1]]
    end_x, end_y = move[2], move[3]

    chess_board[end_x][end_y] = piece
    chess_board[move[0]][move[1]] = 0

    # promoting pawn on the last rank to queen
    if is_white_turn and piece == 1 and end_x == 0:
        promoted_piece = pawn_promotion(is_white_turn)
        chess_board[end_x][end_y] = promoted_piece
        print(" White pawn promotes to a queen")

    elif not is_white_turn and piece == 7 and end_x == 7:
        promoted_piece = pawn_promotion(is_white_turn)
        chess_board[end_x][end_y] = promoted_piece
        print(" Black pawn promotes to a queen")

    # updating the king positions in case they were moved
    if chess_board[end_x][end_y] == 6:  # (white king)
        w_king_pos = [end_x, end_y]

        if w_king_pos != chess_board[7][4]:
            w_king_not_moved = False

        # moving the h-file rook for short castle white
        if move[1] == 4 and chess_board[7][move[3]] == chess_board[7][6]:
            if chess_board[0][6] == 6:
                chess_board[7][5] = chess_board[7][7]
                chess_board[7][7] = 0
        # moving the a-file rook for long castle white
        if move[1] == 4 and chess_board[7][move[3]] == chess_board[7][2]:
            if chess_board[0][6] == 6:
                chess_board[7][3] = chess_board[7][0]
                chess_board[7][0] = 0

    elif chess_board[end_x][end_y] == 12:  # (black king)
        b_king_pos = [end_x, end_y]

        if b_king_pos != chess_board[0][4]:
            b_king_not_moved = False

        # moving the h-file rook for short castle black
        if move[1] == 4 and chess_board[0][move[3]] == chess_board[0][6]:
            if chess_board[0][6] == 12:
                chess_board[0][5] = chess_board[0][7]
                chess_board[0][7] = 0
        # moving the a-file rook for long castle black
        if move[1] == 4 and chess_board[0][move[3]] == chess_board[0][2]:
            if chess_board[0][6] == 12:
                chess_board[0][3] = chess_board[0][0]
                chess_board[0][0] = 0

    if chess_board[end_x][end_y] == 2:
        if move[1] == 7:
            w_h_rook_not_moved = False
    if chess_board[end_x][end_y] == 2:
        if move[1] == 0:
            w_a_rook_not_moved = False
    if chess_board[end_x][end_y] == 8:
        if move[1] == 7:
            b_h_rook_not_moved = False
    if chess_board[end_x][end_y] == 8:
        if move[1] == 0:
            b_a_rook_not_moved = False

    print_updated_chess_board(chess_board)


def print_updated_chess_board(chess_board):
    piece_symbols = {0: '0', 1: 'P', 2: 'R', 3: 'N', 4: 'B', 5: 'Q', 6: 'K',
                     7: 'p', 8: 'r', 9: 'n', 10: 'b', 11: 'q', 12: 'k'}
    print("Current Chess Board:")
    for row in chess_board:
        print(" ".join(piece_symbols.get(piece, str(piece)) for piece in row))
    print("\n")


# ------------------------------------- 3. Define function to check chess board and piece -----------------------


def get_white_possible_moves(chess_board):
    white_possible_moves = []

    for x in range(8):
        for y in range(8):
            piece = chess_board[x][y]

            if piece == 1:
                white_possible_moves.append(white_pawn_movement(chess_board, x, y))
            elif piece == 2:
                white_possible_moves.append(white_horizontal_movement(chess_board, x, y))
                white_possible_moves.append(white_vertical_movement(chess_board, x, y))
            elif piece == 3:
                white_possible_moves.append(white_knight_movement(chess_board, x, y))
            elif piece == 4:
                white_possible_moves.append(white_diagonal_movement(chess_board, x, y))
            elif piece == 5:
                white_possible_moves.append(white_horizontal_movement(chess_board, x, y))
                white_possible_moves.append(white_vertical_movement(chess_board, x, y))
                white_possible_moves.append(white_diagonal_movement(chess_board, x, y))
            elif piece == 6:
                white_possible_moves.append(white_king_movement(chess_board, x, y))

    return white_possible_moves


def get_white_legal_moves(chess_board):
    white_legal_moves = []
    flattened_white_possible_moves = get_white_possible_moves(chess_board)
    flattened_white_possible_moves = [t for xs in flattened_white_possible_moves for t in xs]

    for move in flattened_white_possible_moves:
        current_x, current_y, new_x, new_y = move
        if is_move_legal(chess_board, move, is_white_turn):
            white_legal_moves.append(move)
    # print(white_legal_moves)

    return white_legal_moves


def get_black_possible_moves(chess_board):
    black_possible_moves = []

    for x in range(8):
        for y in range(8):
            piece = chess_board[x][y]

            if piece == 7:
                black_possible_moves.append(black_pawn_movement(chess_board, x, y))
            elif piece == 8:
                black_possible_moves.append(black_horizontal_movement(chess_board, x, y))
                black_possible_moves.append(black_vertical_movement(chess_board, x, y))
            elif piece == 9:
                black_possible_moves.append(black_knight_movement(chess_board, x, y))
            elif piece == 10:
                black_possible_moves.append(black_diagonal_movement(chess_board, x, y))
            elif piece == 11:
                black_possible_moves.append(black_horizontal_movement(chess_board, x, y))
                black_possible_moves.append(black_vertical_movement(chess_board, x, y))
                black_possible_moves.append(black_diagonal_movement(chess_board, x, y))
            elif piece == 12:
                black_possible_moves.append(black_king_movement(chess_board, x, y))

    return black_possible_moves


def get_black_legal_moves(chess_board):
    black_legal_moves = []
    flattened_black_possible_moves = get_black_possible_moves(chess_board)
    flattened_black_possible_moves = [t for xs in flattened_black_possible_moves for t in xs]

    for move in flattened_black_possible_moves:
        current_x, current_y, new_x, new_y = move
        if is_move_legal(chess_board, move, is_white_turn):
            black_legal_moves.append(move)

    return black_legal_moves


# ---------------------------------- 4. Define different movement functions ------------------------------


def white_pawn_movement(chess_board, x, y):
    white_pawn_moves = []

    if 0 < x:
        # moving forward if space ahead is empty
        if chess_board[x - 1][y] == 0:
            white_pawn_moves.append([x, y, x - 1, y])
        # capturing the piece diagonally right
        if 0 <= y < 7 and 6 < chess_board[x - 1][y + 1] < 13:
            white_pawn_moves.append([x, y, x - 1, y + 1])
        # Capturing the piece diagonally left
        if 0 < y <= 7 and 6 < chess_board[x - 1][y - 1] < 13:
            white_pawn_moves.append([x, y, x - 1, y - 1])
        # moving forward 2 spaces if in original position and both are empty
        if x == 6 and chess_board[x - 1][y] == 0 and chess_board[x - 2][y] == 0:
            white_pawn_moves.append([x, y, x - 2, y])

    return white_pawn_moves


def black_pawn_movement(chess_board, x, y):
    black_pawn_moves = []

    if x < 7:
        # moving forward if space ahead is empty
        if chess_board[x + 1][y] == 0:
            black_pawn_moves.append([x, y, x + 1, y])
        # capturing the piece diagonally right
        if 0 <= y < 7 and 0 < chess_board[x + 1][y + 1] < 7:
            black_pawn_moves.append([x, y, x + 1, y + 1])
        # Capturing the piece diagonally left
        if 0 < y <= 7 and 0 < chess_board[x + 1][y - 1] < 7:
            black_pawn_moves.append([x, y, x + 1, y - 1])
        # moving forward 2 spaces if in original position and both are empty
        if x == 1 and chess_board[x + 1][y] == 0 and chess_board[x + 2][y] == 0:
            black_pawn_moves.append([x, y, x + 2, y])

    return black_pawn_moves


def white_knight_movement(chess_board, x, y):
    white_knight_moves = []

    knight_moves = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1))
    for (j, k) in knight_moves:
        if 7 >= x + j >= 0 and 7 >= y + k >= 0:
            if chess_board[x + j][y + k] == 0:
                white_knight_moves.append([x, y, x + j, y + k])
            elif 6 < chess_board[x + j][y + k] < 13:
                white_knight_moves.append([x, y, x + j, y + k])

    return white_knight_moves


def black_knight_movement(chess_board, x, y):
    black_knight_moves = []

    knight_moves = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1))
    for (j, k) in knight_moves:
        if 7 >= x + j >= 0 and 7 >= y + k >= 0:
            if chess_board[x + j][y + k] == 0:
                black_knight_moves.append([x, y, x + j, y + k])
            elif 0 < chess_board[x + j][y + k] < 7:
                black_knight_moves.append([x, y, x + j, y + k])

    return black_knight_moves


def white_horizontal_movement(chess_board, x, y):
    white_horizontal_moves = []

    # horizontal movement to the right:
    for j in range(1, 8 - y):
        new_y = y + j
        if 0 <= new_y < 8:
            # checking for empty squares:
            if chess_board[x][new_y] == 0:
                white_horizontal_moves.append(([x, y, x, new_y]))
            # checking for squares with opposing pieces:
            elif 6 < chess_board[x][new_y] < 13:
                white_horizontal_moves.append(([x, y, x, new_y]))
                break
            # breaking the function when the only option is for a friendly piece to be ahead
            else:
                break

    # horizontal movement to the left:
    for k in range(1, y + 1):
        new_y = y - k
        if 0 <= new_y < 8:
            if chess_board[x][new_y] == 0:
                white_horizontal_moves.append(([x, y, x, new_y]))
            elif 6 < chess_board[x][new_y] < 13:
                white_horizontal_moves.append(([x, y, x, new_y]))
                break
            else:
                break

    return white_horizontal_moves


def black_horizontal_movement(chess_board, x, y):
    black_horizontal_moves = []
    # horizontal movement to the right:
    for j in range(1, 8 - y):
        new_y = y + j
        if 0 <= new_y < 8:
            # checking for empty squares:
            if chess_board[x][new_y] == 0:
                black_horizontal_moves.append([x, y, x, new_y])
            # checking for squares with opposing pieces:
            elif 0 < chess_board[x][new_y] < 7:
                black_horizontal_moves.append([x, y, x, new_y])
                break
            # breaking the function when the only option is for a friendly piece to be ahead
            else:
                break

    # horizontal movement to the left:
    for k in range(1, y + 1):
        new_y = y - k
        if 0 <= new_y < 8:
            if chess_board[x][new_y] == 0:
                black_horizontal_moves.append([x, y, x, new_y])
            elif 0 < chess_board[x][new_y] < 7:
                black_horizontal_moves.append([x, y, x, new_y])
                break
            else:
                break

    return black_horizontal_moves


def white_vertical_movement(chess_board, x, y):
    white_vertical_moves = []

    for j in range(1, 8 - x):
        new_x = x + j
        if 0 <= new_x < 8:
            if chess_board[new_x][y] == 0:
                white_vertical_moves.append([x, y, new_x, y])
            elif 6 < chess_board[new_x][y] < 13:
                white_vertical_moves.append([x, y, new_x, y])
                break
            else:
                break
    for k in range(1, x + 1):
        new_x = x - k
        if 0 <= new_x < 8:
            if chess_board[new_x][y] == 0:
                white_vertical_moves.append([x, y, new_x, y])
            elif 6 < chess_board[new_x][y] < 13:
                white_vertical_moves.append([x, y, new_x, y])
                break
            else:
                break

    return white_vertical_moves


# vertical movement function for white queen, rook


def black_vertical_movement(chess_board, x, y):
    black_vertical_moves = []

    for j in range(1, 8 - x):
        new_x = x + j
        if 0 <= new_x < 8:
            if chess_board[new_x][y] == 0:
                black_vertical_moves.append([x, y, new_x, y])
            elif 0 < chess_board[new_x][y] < 7:
                black_vertical_moves.append([x, y, new_x, y])
                break
            else:
                break
    for k in range(1, x + 1):
        new_x = x - k
        if 0 <= new_x < 8:
            if chess_board[new_x][y] == 0:
                black_vertical_moves.append([x, y, new_x, y])
            elif 0 < chess_board[new_x][y] < 7:
                black_vertical_moves.append([x, y, new_x, y])
                break
            else:
                break

    return black_vertical_moves


# vertical movement function for black queen, rook


def white_diagonal_movement(chess_board, x, y):
    white_diagonal_moves = []

    # diagonal movement to the top left(-x, -y)
    for j in range(1, 8):
        new_x, new_y = x - j, y - j
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                white_diagonal_moves.append([x, y, new_x, new_y])
            elif 6 < chess_board[new_x][new_y] < 13:
                white_diagonal_moves.append([x, y, new_x, new_y])
                break
            else:
                break
    # diagonal movement to the top right(-x, +y)
    for k in range(1, 8):
        new_x, new_y = x - k, y + k
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                white_diagonal_moves.append([x, y, new_x, new_y])
            elif 6 < chess_board[new_x][new_y] < 13:
                white_diagonal_moves.append([x, y, new_x, new_y])
                break
            else:
                break
    # diagonal movement to the bottom right( +x, +y)
    for m in range(1, 8):
        new_x, new_y = x + m, y + m
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                white_diagonal_moves.append([x, y, new_x, new_y])
            elif 6 < chess_board[new_x][new_y] < 13:
                white_diagonal_moves.append([x, y, new_x, new_y])
                break
            else:
                break
    # diagonal movement to the bottom left( +x, -y)
    for n in range(1, 8):
        new_x, new_y = x + n, y - n
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                white_diagonal_moves.append([x, y, new_x, new_y])
            elif 6 < chess_board[new_x][new_y] < 13:
                white_diagonal_moves.append([x, y, new_x, new_y])
                break
            else:
                break

    return white_diagonal_moves


def black_diagonal_movement(chess_board, x, y):
    black_diagonal_moves = []

    # diagonal movement to the top left(-x, -y)
    for j in range(1, 8):
        new_x, new_y = x - j, y - j  # moving x up and y left
        if 0 <= new_x < 8 and 0 <= new_y < 8:  # checking that x and y are within the chessboard
            # print(f"Checking position: {new_x}, {new_y} -> {chess_board[new_x][new_y]}")
            if chess_board[new_x][new_y] == 0:  # checking for an empty square
                black_diagonal_moves.append([x, y, new_x, new_y])
                # print(f"Empty square: {new_x}, {new_y} -> {chess_board[new_x][new_y]}")
            elif 0 < chess_board[new_x][new_y] < 7:  # checking for a white piece to take
                black_diagonal_moves.append([x, y, new_x, new_y])
                # print(f"Captured at: {new_x}, {new_y}")
                break  # breaking after taking the piece
            else:  # last possibility is a friendly piece, so the function breaks
                # print(f"Friendly piece at: {new_x}, {new_y}")
                break
    # diagonal movement to the top right(-x, +y)
    for k in range(1, 8):
        new_x, new_y = x - k, y + k
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                black_diagonal_moves.append([x, y, new_x, new_y])
            elif 0 < chess_board[new_x][new_y] < 7:
                black_diagonal_moves.append([x, y, new_x, new_y])
                break
            else:
                break
    # diagonal movement to the bottom right( +x, +y)
    for m in range(1, 8):
        new_x, new_y = x + m, y + m
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                black_diagonal_moves.append([x, y, new_x, new_y])
            elif 0 < chess_board[new_x][new_y] < 7:
                black_diagonal_moves.append([x, y, new_x, new_y])
                break
            else:
                break
    # diagonal movement to the bottom left( +x, -y)
    for n in range(1, 8):
        new_x, new_y = x + n, y - n
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                black_diagonal_moves.append([x, y, new_x, new_y])
            elif 0 < chess_board[new_x][new_y] < 7:
                black_diagonal_moves.append([x, y, new_x, new_y])
                break
            else:
                break

    return black_diagonal_moves


def white_king_movement(chess_board, x, y):
    white_king_moves = []

    king_moves = ((1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1))

    for (j, k) in king_moves:
        if 7 >= x + j >= 0 and 7 >= y + k >= 0:
            if not 0 < chess_board[x + j][y + k] < 7:
                white_king_moves.append([x, y, x + j, y + k])

    return white_king_moves


def castling_white(chess_board, x, y):
    b_possible_moves = get_black_possible_moves(chess_board)
    castling_moves = []
    filtered_moves = [move for move in b_possible_moves if len(move) >= 4]

    if w_king_not_moved:
        if w_h_rook_not_moved:
            if chess_board[7][5] == 0 and chess_board[7][6] == 0:
                if [7, 4] not in [[move[2], move[3]] for move in filtered_moves] and \
                        [7, 5] not in [[move[2], move[3]] for move in filtered_moves] and \
                        [7, 6] not in [[move[2], move[3]] for move in filtered_moves]:
                    castling_moves.append([x, y, 7, 6])
        if w_a_rook_not_moved:
            if chess_board[7][2] == 0 and chess_board[7][3] == 0:
                if [7, 4] not in [[move[2], move[3]] for move in filtered_moves] and \
                        [7, 2] not in [[move[2], move[3]] for move in filtered_moves] and \
                        [7, 3] not in [[move[2], move[3]] for move in filtered_moves]:
                    castling_moves.append([x, y, 7, 2])

    return castling_moves


def black_king_movement(chess_board, x, y):
    black_king_moves = []
    king_moves = ((1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1))

    for (j, k) in king_moves:
        if 7 >= x + j >= 0 and 7 >= y + k >= 0:
            if not 6 < chess_board[x + j][y + k] < 13:
                black_king_moves.append([x, y, x + j, y + k])

    return black_king_moves


def castling_black(chess_board, x, y):
    w_possible_moves = get_white_possible_moves(chess_board)
    castling_moves = []
    filtered_moves = [move for move in w_possible_moves if len(move) >= 4]

    if b_king_not_moved:
        if b_h_rook_not_moved:
            if chess_board[0][5] == 0 and chess_board[0][6] == 0:
                if [0, 4] not in [[move[2], move[3]] for move in filtered_moves] and \
                        [0, 5] not in [[move[2], move[3]] for move in filtered_moves] and \
                        [0, 6] not in [[move[2], move[3]] for move in filtered_moves]:
                    castling_moves.append([x, y, 0, 6])
        if w_a_rook_not_moved:
            if chess_board[0][2] == 0 and chess_board[0][3] == 0:
                if [0, 4] not in [[move[2], move[3]] for move in filtered_moves] and \
                        [0, 2] not in [[move[2], move[3]] for move in filtered_moves] and \
                        [0, 3] not in [[move[2], move[3]] for move in filtered_moves]:
                    castling_moves.append([x, y, 0, 2])

    return castling_moves

    # ----------------------------------------- Move Evaluation Algorythm -------------------------------


def minimax(chess_board, depth, is_white_turn, alpha, beta):
    if depth == 0:
        return evaluate_board_state(chess_board, is_white_turn)

    game_state = is_check_mate(chess_board, is_white_turn)
    if game_state == 'Checkmate':
        if is_white_turn:
            return float('inf')
        else:
            return float('-inf')

    elif game_state == 'Stalemate':
        return 0

    if is_white_turn:
        max_eval = float('-inf')
        white_legal_moves = get_white_legal_moves(chess_board)

        for move in white_legal_moves:
            temp_board = simulate_move(chess_board, move)

            eval = minimax(temp_board, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return max_eval

    else:
        min_eval = float('inf')
        black_legal_moves = get_black_legal_moves(chess_board)

        for move in black_legal_moves:
            temp_board = simulate_move(chess_board, move)

            eval = minimax(temp_board, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break

        return min_eval


def evaluate_board_state(chess_board, is_white_turn):
    piece_values = {1: 1, 2: 5, 3: 3, 4: 3, 5: 8, 6: 20, 7: -1, 8: -5, 9: -3, 10: -3, 11: -8, 12: -20}
    chess_board_state = 0

    white_pawn_board_multiplier = [[8, 8, 8, 8, 8, 8, 8, 8],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1.3, 1.3, 1, 1, 1],
                                   [1, 1, 1.3, 2, 2, 1.3, 1, 1],
                                   [1, 1, 1.3, 2, 2, 1.3, 1, 1],
                                   [1, 1, 1, 1.3, 1.3, 1, 1, 1.2],
                                   [1, 1, 1, 1, 1, 1.5, 1.5, 1.5],
                                   [1, 1, 1, 1, 1, 1, 1, 1]]

    black_pawn_board_multiplier = [[1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1.5, 1.5, 1.5],
                                   [1, 1, 1, 1.3, 1.3, 1, 1, 1.2],
                                   [1, 1, 1.3, 2, 2, 1.3, 1, 1],
                                   [1, 1, 1.3, 2, 2, 1.3, 1, 1],
                                   [1, 1, 1, 1.3, 1.3, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [8, 8, 8, 8, 8, 8, 8, 8]]

    knight_board_multiplier = [[0.5, 0.9, 0.7, 0.7, 0.7, 0.7, 0.9, 0.5],
                               [0.6, 0.8, 0.9, 0.9, 0.9, 0.9, 0.8, 0.6],
                               [0.7, 0.9, 1.2, 1, 1, 1.2, 0.9, 0.7],
                               [0.7, 0.9, 1, 1.5, 1.5, 1, 0.9, 0.7],
                               [0.7, 0.9, 1, 1.5, 1.5, 1, 0.9, 0.7],
                               [0.7, 0.9, 1.2, 1, 1, 1.2, 0.9, 0.7],
                               [0.6, 0.8, 0.9, 0.9, 0.9, 0.9, 0.8, 0.6],
                               [0.5, 0.9, 0.7, 0.7, 0.7, 0.7, 0.9, 0.5]]

    bishop_board_multiplier = [[1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 1.2, 1.2, 1, 1, 1],
                               [1, 1.4, 1.4, 1.2, 1.2, 1.4, 1.4, 1],
                               [1, 1.4, 1.4, 1.2, 1.2, 1.4, 1.4, 1],
                               [1, 1, 1, 1.2, 1.2, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1]]

    rook_board_multiplier = [[1, 1, 1, 1.1, 1.1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1.1, 1.1, 1, 1, 1]]

    queen_board_multiplier = [[1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1.1, 1, 1],
                              [1, 1, 1, 1.1, 1, 1.1, 1, 1],
                              [1, 1, 1, 1.1, 1.1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1.1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1]]

    king_board_multiplier = [[1, 1, 1.02, 1, 1, 1, 1.06, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1.02, 1, 1, 1, 1.06, 1]]

    board_multiplier = {1: white_pawn_board_multiplier, 7: black_pawn_board_multiplier,
                        3: knight_board_multiplier, 9: knight_board_multiplier,
                        4: bishop_board_multiplier, 10: bishop_board_multiplier,
                        2: rook_board_multiplier, 8: rook_board_multiplier,
                        5: queen_board_multiplier, 11: queen_board_multiplier,
                        6: king_board_multiplier, 12: king_board_multiplier}

    for x in range(8):
        for y in range(8):
            piece = chess_board[x][y]
            if piece != 0:
                piece_value = piece_values.get(piece)
                chosen_multiplier = board_multiplier.get(piece)
                if chosen_multiplier:
                    position_multiplier = chosen_multiplier[x][y]

                    chess_board_state += piece_value * position_multiplier

    game_state = is_check_mate(chess_board, is_white_turn)
    if game_state == 'Checkmate':
        if is_white_turn:
            chess_board_state = -1000
        else:
            chess_board_state = 1000
    elif game_state == 'Stalemate':
        chess_board_state = 0

    return chess_board_state


def find_best_move(chess_board, is_white_turn, depth, eval_diff=0.1):
    best_move = None
    top_moves = []
    if is_white_turn:
        max_eval = float('-inf')
        white_legal_moves = get_white_legal_moves(chess_board)

        x, y = None, None
        for i in range(8):
            for j in range(8):
                if chess_board[i][j] == 6:
                    x, y = i, j
                    break
            if x is not None:
                break

        white_legal_moves.extend(castling_white(chess_board, x, y))

        for move in white_legal_moves:
            temp_board = simulate_move(chess_board, move)

            eval = minimax(temp_board, depth - 1, False, float('-inf'), float('inf'))

            if eval > max_eval:
                max_eval = eval
                top_moves = [move]
            elif abs(eval - max_eval) < eval_diff:
                top_moves.append(move)

                # if best_move:
            # print("+++", top_moves)
            best_move = random.choice(top_moves)

    else:
        min_eval = float('inf')
        black_legal_moves = get_black_legal_moves(chess_board)

        x, y = None, None
        for i in range(8):
            for j in range(8):
                if chess_board[i][j] == 12:
                    x, y = i, j
                    break
            if x is not None:
                break

        black_legal_moves.extend(castling_black(chess_board, x, y))

        for move in black_legal_moves:
            temp_board = simulate_move(chess_board, move)

            eval = minimax(temp_board, depth - 1, True, float('-inf'), float('inf'))

            if eval < min_eval:
                min_eval = eval
                top_moves = [move]
            elif abs(eval - min_eval) < eval_diff:
                top_moves.append(move)

                # if best_move:
            print("+++", top_moves)
            best_move = random.choice(top_moves)

    return best_move


# ----------------------------------------- Main Function -------------------------------------------

def get_player_move():
    running = True
    selected_square = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Close the window when the user quits
                pygame.quit()
                return None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_square_under_mouse(pos)
                if selected_square is None:
                    # First click: select the piece (starting position)
                    selected_square = (row, col)
                    # Highlight the selected square
                    pygame.draw.rect(screen, pygame.Color("green"),
                                     pygame.Rect(col * square_size, row * square_size, square_size, square_size), 3)
                else:
                    # Second click: set the target (ending position)
                    to_square = (row, col)
                    # Return both starting and target positions
                    return selected_square[0], selected_square[1], to_square[0], to_square[1]

        pygame.display.flip()


def game_loop(screen, chess_board, depth):
    running = True

    print("Choose game mode:")
    print("1. Play as White")
    print("2. Play as Black")
    print("3. AI vs AI")
    #print("4. Player vs Player")

    player_is_white = False
    player_is_black = False
    ai_vs_ai = False

    game_mode = input("Enter 1, 2, 3: ")

    if game_mode not in ['1', '2', '3']:
        print("Invalid selection, Please enter 1, 2, 3")

    if game_mode == '1':
        player_is_white = True
    if game_mode == '2':
        player_is_black = True
    if game_mode == '3':
        ai_vs_ai = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        visualize_game_state(screen)
        pygame.display.flip()
        # for i in range(8):
        # print(chess_board[i])
        if is_white_turn:
            print(" Its Whites turn!")
            if is_king_in_check(chess_board, is_white_turn):
                print(" White king is in check")

            if player_is_white:
                game_state = is_check_mate(chess_board, is_white_turn)
                if game_state == 'Checkmate':
                    print(" Checkmate for Black!")
                    running = False
                    break
                if game_state == 'Stalemate':
                    print(" Draw by Stalemate!")
                    running = False
                    break

                white_choice = get_player_move()
                if white_choice:
                    update_chess_board(chess_board, white_choice, is_white_turn)

            else:
                best_move = find_best_move(chess_board, is_white_turn, depth)
                if best_move:
                    white_choice = best_move
                    piece_int = chess_board[white_choice[0]][white_choice[1]]
                    piece_str = w_piece_dict.get(piece_int)
                    print(f" White moves {piece_str} from "
                          f"{white_choice[0], white_choice[1]} to --> {white_choice[2], white_choice[3]}")
                    update_chess_board(chess_board, white_choice, is_white_turn)
                else:
                    game_state = is_check_mate(chess_board, is_white_turn)
                    if game_state == 'Checkmate':
                        print(" Checkmate for Black!")
                        running = False
                        break
                    if game_state == 'Stalemate':
                        print(" Draw by Stalemate!")
                        running = False
                        break


            visualize_game_state(screen)
            pygame.display.flip()
            print(" Current state of the board:", evaluate_board_state(chess_board, is_white_turn))
            changing_turns()

        else:
            print(" It´s Blacks turn!")
            if is_king_in_check(chess_board, is_white_turn):
                print(" Black king is in check")

            if player_is_black:
                game_state = is_check_mate(chess_board, is_white_turn)
                if game_state == 'Checkmate':
                    print(" Checkmate for White!")
                    running = False
                    break
                if game_state == 'Stalemate':
                    print(" Draw by Stalemate!")
                    running = False
                    break

                black_choice = get_player_move()
                if black_choice:
                    update_chess_board(chess_board, black_choice, is_white_turn)

            else:

                best_move = find_best_move(chess_board, is_white_turn, depth)
                if best_move:
                    black_choice = best_move
                    piece_int = chess_board[black_choice[0]][black_choice[1]]
                    piece_str = b_piece_dict.get(piece_int)
                    print(f" Black moves {piece_str} from "
                          f"{black_choice[0], black_choice[1]} to --> {black_choice[2], black_choice[3]}")
                    update_chess_board(chess_board, black_choice, is_white_turn)
                else:
                    game_state = is_check_mate(chess_board, is_white_turn)
                    if game_state == 'Checkmate':
                        print(" Checkmate for White!")
                        running = False
                        break
                    if game_state == 'Stalemate':
                        print(" Draw by Stalemate!")
                        running = False
                        break

            visualize_game_state(screen)
            pygame.display.flip()
            print(" Current state of the board:", evaluate_board_state(chess_board, is_white_turn))
            changing_turns()

    pygame.quit()


if __name__ == '__main__':
    pygame.init()

    width = 800
    height = 800
    dimensions = 8
    square_size = 100
    square = height // dimensions
    screen = pygame.display.set_mode((width, height))
    screen.fill(pygame.Color("white"))
    pygame.time.Clock().tick(10)

    depth = 4

    game_loop(screen, chess_board, depth)

