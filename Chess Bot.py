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
#       - add a timer to see how long the program needs to make a move *
#       - add en passant
#       - fix castling bug *
#       - improve UI to only allow legal moves to be considered inputs and highlight legal moves
#       - add promotion rule to pawns *
#       - run tests to check for edge cases and make sure the logic is correct *
#       - start working on move evaluation algorythm:
#           1. minimax system *
#           2. weights for pieces *
#           3. "heatmap" masks for each individual piece *
#           4. implement checkmate into evaluation       *
#           5. tempo/ zugzwang weighing ( pointless / already covered in move simulation?)
#           6. moving a piece should make consecutive moves with the same piece weigh less
#           7. friendly pieces defending each other/ attacking same enemy position weigh more   // Prio
#           8. pins on heavy pieces good
#           9. trade pieces when ahead to simplify position
#          10. calculate checks deeper into possible checkmates         // Prio
#       - ideas to make calculation more efficient:
#           1. alpha beta pruning *
#           3. prioritize checks/heavy pieces/positions on the board *
#           4. procedural weight map changes according to turn count
#           5. board hashing to prevent simulation for same board outcomes *
#           6. magic bit board?
#           7. precomputation // prio

from itertools import chain
import cProfile
import pstats
import random
import time

import pygame

depth = 2

player_is_white = False
player_is_black = False
ai_vs_ai = False

empty_square = 0
w_piece_dict = {1: 'w_pawn', 2: 'w_rook', 3: 'w_knight', 4: 'w_bishop', 5: 'w_queen', 6: 'w_king'}
b_piece_dict = {7: 'b_pawn', 8: 'b_rook', 9: 'b_knight', 10: 'b_bishop', 11: 'b_queen', 12: 'b_king'}

computed_moves_cache = {}

w_king_pos = [7, 4]
b_king_pos = [0, 4]

precomputed_w_p_moves = {}
precomputed_b_p_moves = {}
precomputed_knight_moves = {}
precomputed_horizontal_moves = {}
precomputed_vertical_moves = {}
precomputed_diagonal_moves = {}
precomputed_king_moves = {}

w_short_castle = False
w_long_castle = False
b_short_castle = False
b_long_castle = False

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
chess_board = [[0, 0, 0, 0, 12, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 4, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 3, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 6, 0, 0, 0]]

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
        legal_moves = get_black_possible_moves(chess_board)
    else:
        legal_moves = get_white_possible_moves(chess_board)

    return legal_moves


def is_king_in_check(temp_board, is_white_turn):
    king_value = 6 if is_white_turn else 12
    king_pos = find_king(temp_board, king_value)

    if king_pos is None:
        return True

    opponents_moves = generate_opponents_moves(temp_board, is_white_turn)
    # print(f"King position: {king_pos}")
    # print("Opponent's moves:", opponents_moves)
    for move in opponents_moves:
        # Ensure move is a list or tuple with at least four elements
        if isinstance(move, (list, tuple)) and len(move) >= 4:
            if move[2] == king_pos[0] and move[3] == king_pos[1]:
                return True
        """else:
            print(f"Unexpected move format: {move}")"""

    return False


def is_check_mate(chess_board, is_white_turn):
    if is_white_turn:
        if not get_black_legal_moves(chess_board, not is_white_turn):
            if is_king_in_check(chess_board, False):
                forced_mate_eval = minimax(chess_board, depth, not is_white_turn, float('-inf'), float('inf'))
                if forced_mate_eval == float('inf'):
                    return 'Checkmate'
            else:
                return 'Stalemate'

    else:
        if not get_white_legal_moves(chess_board, not is_white_turn):
            if is_king_in_check(chess_board, True):
                forced_mate_eval = minimax(chess_board, depth, not is_white_turn, float('-inf'), float('inf'))
                if forced_mate_eval == float('-inf'):
                    return 'Checkmate'
            else:
                return 'Stalemate'

    return None


def simulate_move(chess_board, move):
    if not (isinstance(move, (list, tuple)) and len(move) == 4):
        print(f"Unexpected move format in simulate_move: {move}")
        return chess_board  # Return board unmodified if move format is wrong
    # Create a deep copy of the board
    temp_board = [row[:] for row in chess_board]

    start_x, start_y, end_x, end_y = move
    temp_board[end_x][end_y] = temp_board[start_x][start_y]

    # print(f"Simulating move: {move} for piece: {piece}")

    temp_board[start_x][start_y] = 0

    """print("Board state after simulated move:")
    for row in temp_board:
        print(row)"""

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


def find_king(chess_board, king_value):
    for x in range(8):
        for y in range(8):
            if chess_board[x][y] == king_value:
                return x, y

    return None


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
            if chess_board[7][6] == 6:
                chess_board[7][5] = chess_board[7][7]
                chess_board[7][7] = 0
        # moving the a-file rook for long castle white
        if move[1] == 4 and chess_board[7][move[3]] == chess_board[7][2]:
            if chess_board[7][2] == 6:
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
            if chess_board[0][2] == 12:
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
                moves = white_pawn_movement(chess_board, x, y)
            elif piece == 2:
                moves = (white_horizontal_movement(chess_board, x, y) +
                         white_vertical_movement(chess_board, x, y))
            elif piece == 3:
                moves = white_knight_movement(chess_board, x, y)

            elif piece == 4:
                moves = white_diagonal_movement(chess_board, x, y)

            elif piece == 5:
                moves = (white_horizontal_movement(chess_board, x, y) +

                         white_vertical_movement(chess_board, x, y) +

                         white_diagonal_movement(chess_board, x, y))

            elif piece == 6:
                moves = white_king_movement(chess_board, x, y)
            else:
                moves = []

            if all(isinstance(m, list) and len(m) == 4 for m in moves):
                white_possible_moves.extend(moves)
            else:
                print(f"Unexpected move format in {piece} movement at {(x, y)}: {moves}")

    return white_possible_moves


def get_white_legal_moves(chess_board, is_white_turn):
    white_legal_moves = []
    white_flattened_possible_moves = get_white_possible_moves(chess_board)
    white_flattened_possible_moves = [move for moves in [white_flattened_possible_moves] for move in moves]

    for move in white_flattened_possible_moves:
        start_x, start_y, new_x, new_y = move
        if is_move_legal(chess_board, move, is_white_turn):
            white_legal_moves.append(move)

    return white_legal_moves


def get_black_possible_moves(chess_board):
    black_possible_moves = []
    for x in range(8):
        for y in range(8):
            piece = chess_board[x][y]

            if piece == 7:
                moves = black_pawn_movement(chess_board, x, y)
            elif piece == 8:
                moves = (black_horizontal_movement(chess_board, x, y) +
                         black_vertical_movement(chess_board, x, y))
            elif piece == 9:
                moves = black_knight_movement(chess_board, x, y)
            elif piece == 10:
                moves = black_diagonal_movement(chess_board, x, y)
            elif piece == 11:
                moves = (black_horizontal_movement(chess_board, x, y) +
                         black_vertical_movement(chess_board, x, y) +
                         black_diagonal_movement(chess_board, x, y))
            elif piece == 12:
                moves = black_king_movement(chess_board, x, y)
            else:
                moves = []

            if all(isinstance(m, list) and len(m) == 4 for m in moves):
                black_possible_moves.extend(moves)
            else:
                print(f"Unexpected move format in {piece} movement at {(x, y)}: {moves}")

    return black_possible_moves


def get_black_legal_moves(chess_board, is_white_turn):
    black_legal_moves = []
    flattened_black_possible_moves = get_black_possible_moves(chess_board)
    flattened_black_possible_moves = [t for xs in [flattened_black_possible_moves] for t in xs]

    for move in flattened_black_possible_moves:
        if is_move_legal(chess_board, move, is_white_turn):
            black_legal_moves.append(move)

    return black_legal_moves


# ---------------------------------- 4. Define different movement functions ------------------------------


def precompute_white_pawn_moves():
    for x in range(8):
        for y in range(8):
            moves = []

            if x > 0:
                moves.append((x - 1, y))
            if x == 6:
                moves.append((x - 2, y))
            if x > 0 and y < 7:
                moves.append((x - 1, y + 1))
            if x > 0 and y > 0:
                moves.append((x - 1, y - 1))

            precomputed_w_p_moves[(x, y)] = moves


def white_pawn_movement(chess_board, x, y):
    white_pawn_moves = []
    precomputed_moves = precomputed_w_p_moves[(x, y)]

    white_pawn_moves.extend([
        [x, y, new_x, new_y]
        for new_x, new_y in precomputed_moves
        if new_y == y and 8 > new_x >= 0 == chess_board[new_x][new_y]
           and not (x == 6 and new_x == x - 2 and chess_board[x - 1][y] != 0)
    ])

    white_pawn_moves.extend([
        [x, y, new_x, new_y]
        for new_x, new_y in precomputed_moves
        if abs(new_y - y) == 1 and 0 <= new_x < 8 and 0 <= new_y < 8
           and 6 < chess_board[new_x][new_y] < 13
    ])

    return white_pawn_moves


def precompute_black_pawn_moves():
    for x in range(8):
        for y in range(8):
            moves = []

            if x > 0:
                moves.append((x + 1, y))
            if x == 1:
                moves.append((x + 2, y))
            if x > 0 and y < 7:
                moves.append((x + 1, y + 1))
            if x > 0 and y > 0:
                moves.append((x + 1, y - 1))

            precomputed_b_p_moves[(x, y)] = moves


def black_pawn_movement(chess_board, x, y):
    black_pawn_moves = []
    precomputed_moves = precomputed_b_p_moves[(x, y)]

    black_pawn_moves.extend([
        [x, y, new_x, new_y]
        for new_x, new_y in precomputed_moves
        if new_y == y and 8 > new_x >= 0 == chess_board[new_x][new_y]
           and not (x == 1 and new_x == x + 2 and chess_board[x + 1][y] != 0)
    ])

    black_pawn_moves.extend([
        [x, y, new_x, new_y]
        for new_x, new_y in precomputed_moves
        if abs(new_y - y) == 1 and 0 <= new_x < 8 and 0 <= new_y < 8
           and 0 < chess_board[new_x][new_y] < 7
    ])
    return black_pawn_moves


def precompute_knight_moves():
    for x in range(8):
        for y in range(8):
            moves = []
            knight_moves = ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))

            for (j, k) in knight_moves:
                if 7 >= x + j >= 0 and 7 >= y + k >= 0:
                    if chess_board[x + j][y + k] == 0:
                        moves.append((x + j, y + k))

            precomputed_knight_moves[(x, y)] = moves


def white_knight_movement(chess_board, x, y):
    white_knight_moves = []
    precomputed_moves = precomputed_knight_moves[(x, y)]

    white_knight_moves.extend([
        [x, y, new_x, new_y]
        for new_x, new_y in precomputed_moves
        if chess_board[x][y] == 0
        if 6 < chess_board[new_x][new_y] < 13
    ])

    return white_knight_moves


def black_knight_movement(chess_board, x, y):
    black_knight_moves = []
    precomputed_moves = precomputed_knight_moves[(x, y)]

    black_knight_moves.extend([
        [x, y, new_x, new_y]
        for new_x, new_y in precomputed_moves
        if chess_board[x][y] == 0
        if 0 < chess_board[new_x][new_y] < 7
    ])

    return black_knight_moves


def generate_white_directional_moves(chess_board, x, y, direction_moves):
    for new_x, new_y in direction_moves:
        if chess_board[new_x][new_y] == 0:
            yield [x, y, new_x, new_y]
        elif 6 < chess_board[new_x][new_y] < 13:
            yield [x, y, new_x, new_y]
            break
        else:
            break


def generate_black_directional_moves(chess_board, x, y,direction_moves):
    for new_x, new_y in direction_moves:
        if chess_board[new_x][new_y] == 0:
            yield [x, y, new_x, new_y]
        elif 0 < chess_board[new_x][new_y] < 7:
            yield [x, y, new_x, new_y]
            break
        else:
            break


def precompute_horizontal_moves():
    for x in range(8):
        for y in range(8):
            moves = {"right": [], "left": []}

            for j in range(1, 8 - y):
                moves["right"].append([x, y + j])
            for k in range(1, y + 1):
                moves["left"].append([x, y - k])

            precomputed_horizontal_moves[(x, y)] = moves


def white_horizontal_movement(chess_board, x, y):
    white_horizontal_moves = []
    precomputed_moves = precomputed_horizontal_moves[(x, y)]

    white_horizontal_moves.extend(
        chain(
            generate_white_directional_moves(chess_board, x, y, precomputed_moves["right"]),
            generate_white_directional_moves(chess_board, x, y, precomputed_moves["left"])
        )
    )

    return white_horizontal_moves


def black_horizontal_movement(chess_board, x, y):
    black_horizontal_moves = []
    precomputed_moves = precomputed_horizontal_moves[(x, y)]

    black_horizontal_moves.extend(
        chain(
            generate_black_directional_moves(chess_board, x, y, precomputed_moves["right"]),
            generate_black_directional_moves(chess_board, x, y, precomputed_moves["left"])
        )
    )
    return black_horizontal_moves


def precompute_vertical_moves():
    for x in range(8):
        for y in range(8):
            moves = {"up": [], "down": []}

            # Generate "up" moves within bounds
            for i in range(x - 1, -1, -1):
                moves["up"].append([i, y])

            # Generate "down" moves within bounds
            for i in range(x + 1, 8):
                moves["down"].append([i, y])

            precomputed_vertical_moves[(x, y)] = moves


def white_vertical_movement(chess_board, x, y):
    white_vertical_moves = []
    precomputed_moves = precomputed_vertical_moves[(x, y)]

    for new_x, new_y in precomputed_moves["down"]:
        if chess_board[new_x][new_y] == 0:
            white_vertical_moves.append([x, y, new_x, new_y])
        elif 6 < chess_board[new_x][new_y] < 13:
            white_vertical_moves.append([x, y, new_x, new_y])
            break
        else:
            break

    for new_x, new_y in precomputed_moves["up"]:
        if chess_board[new_x][new_y] == 0:
            white_vertical_moves.append([x, y, new_x, new_y])
        elif 6 < chess_board[new_x][new_y] < 13:
            white_vertical_moves.append([x, y, new_x, new_y])
            break
        else:
            break

    return white_vertical_moves


def black_vertical_movement(chess_board, x, y):
    black_vertical_moves = []
    precomputed_moves = precomputed_vertical_moves[(x, y)]

    for new_x, new_y in precomputed_moves["down"]:
        if chess_board[new_x][new_y] == 0:
            black_vertical_moves.append([x, y, new_x, new_y])
        elif 0 < chess_board[new_x][new_y] < 7:
            black_vertical_moves.append([x, y, new_x, new_y])
            break
        else:
            break

    for new_x, new_y in precomputed_moves["up"]:
        if chess_board[new_x][new_y] == 0:
            black_vertical_moves.append([x, y, new_x, new_y])
        elif 0 < chess_board[new_x][new_y] < 7:
            black_vertical_moves.append([x, y, new_x, new_y])
            break
        else:
            break

    return black_vertical_moves


def precompute_diagonal_moves():
    global precomputed_diagonal_moves

    for x in range(8):
        for y in range(8):
            moves = {"up_left": [], "up_right": [], "down_left": [], "down_right": []}

            for j in range(1, min(x, y) + 1):
                new_x, new_y = x - j, y - j
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    moves["up_left"].append([new_x, new_y])
                else:
                    break
            for j in range(1, min(x, 7 - y) + 1):
                new_x, new_y = x - j, y + j
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    moves["up_right"].append([new_x, new_y])
                else:
                    break
            for j in range(1, min(7 - x, y) + 1):
                new_x, new_y = x + j, y - j
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    moves["down_left"].append([new_x, new_y])
                else:
                    break
            for j in range(1, min(7 - x, 7 - y) + 1):
                new_x, new_y = x + j, y + j
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    moves["down_right"].append([new_x, new_y])
                else:
                    break

            precomputed_diagonal_moves[(x, y)] = moves


def white_diagonal_movement(chess_board, x, y):
    white_diagonal_moves = []
    precomputed_moves = precomputed_diagonal_moves[(x, y)]

    for new_x, new_y in precomputed_moves["up_left"]:
        if chess_board[new_x][new_y] == 0:
            white_diagonal_moves.append([x, y, new_x, new_y])
        elif 6 < chess_board[new_x][new_y] < 13:
            white_diagonal_moves.append([x, y, new_x, new_y])
            break
        else:
            break
    for new_x, new_y in precomputed_moves["up_right"]:
        if chess_board[new_x][new_y] == 0:
            white_diagonal_moves.append([x, y, new_x, new_y])
        elif 6 < chess_board[new_x][new_y] < 13:
            white_diagonal_moves.append([x, y, new_x, new_y])
            break
        else:
            break
    for new_x, new_y in precomputed_moves["down_left"]:
        if chess_board[new_x][new_y] == 0:
            white_diagonal_moves.append([x, y, new_x, new_y])
        elif 6 < chess_board[new_x][new_y] < 13:
            white_diagonal_moves.append([x, y, new_x, new_y])
            break
        else:
            break
    for new_x, new_y in precomputed_moves["down_right"]:
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
    precomputed_moves = precomputed_diagonal_moves[(x, y)]

    for new_x, new_y in precomputed_moves["up_left"]:
        if chess_board[new_x][new_y] == 0:
            black_diagonal_moves.append([x, y, new_x, new_y])
        elif 0 < chess_board[new_x][new_y] < 7:
            black_diagonal_moves.append([x, y, new_x, new_y])
            break
        else:
            break
    for new_x, new_y in precomputed_moves["up_right"]:
        if chess_board[new_x][new_y] == 0:
            black_diagonal_moves.append([x, y, new_x, new_y])
        elif 0 < chess_board[new_x][new_y] < 7:
            black_diagonal_moves.append([x, y, new_x, new_y])
            break
        else:
            break
    for new_x, new_y in precomputed_moves["down_left"]:
        if chess_board[new_x][new_y] == 0:
            black_diagonal_moves.append([x, y, new_x, new_y])
        elif 0 < chess_board[new_x][new_y] < 7:
            black_diagonal_moves.append([x, y, new_x, new_y])
            break
        else:
            break
    for new_x, new_y in precomputed_moves["down_right"]:
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

    king_moves = [(1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1)]

    for (j, k) in king_moves:
        new_x, new_y = x + j, y + k
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                white_king_moves.append([x, y, new_x, new_y])
            if 6 < chess_board[new_x][new_y] < 13:
                temp_board = simulate_move(chess_board, [x, y, new_x, new_y])
                if not is_king_in_check(temp_board, True):
                    white_king_moves.append([x, y, new_x, new_y])
                else:
                    continue

    return white_king_moves


def short_castling_white(chess_board, king_x, king_y):
    b_possible_moves = get_black_possible_moves(chess_board)
    filtered_moves = [move for moves in b_possible_moves for move in moves]
    castle_squares = [[7, 4], [7, 5], [7, 6]]

    if chess_board[7][5] == 0 and chess_board[7][6] == 0:
        if all(square not in [[move[2], move[3]] for move in filtered_moves] for square in castle_squares):
            if w_king_not_moved:
                if chess_board[7][7] == 2:
                    if w_h_rook_not_moved:
                        return True

    return False


def long_castling_white(chess_board, king_x, king_y):
    b_possible_moves = get_black_possible_moves(chess_board)
    filtered_moves = [move for moves in b_possible_moves for move in moves]
    castle_squares = [[7, 4], [7, 3], [7, 2]]

    if chess_board[7][1] == 0 and chess_board[7][2] == 0 and chess_board[7][3] == 0:
        if all(square not in [[move[2], move[3]] for move in filtered_moves] for square in castle_squares):
            if w_king_not_moved:
                if chess_board[7][0] == 2:
                    if w_a_rook_not_moved:
                        return True

    return False


def black_king_movement(chess_board, x, y):
    black_king_moves = []
    king_moves = [(1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1)]

    for (j, k) in king_moves:
        new_x, new_y = x + j, y + k
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if chess_board[new_x][new_y] == 0:
                black_king_moves.append([x, y, new_x, new_y])
            if 0 < chess_board[new_x][new_y] < 7:
                temp_board = simulate_move(chess_board, [x, y, new_x, new_y])
                """for i in range(8):
                    print(temp_board[i])"""
                if not is_king_in_check(temp_board, False):
                    black_king_moves.append([x, y, new_x, new_y])
                else:
                    continue

    return black_king_moves


def short_castling_black(chess_board, king_x, king_y):
    w_possible_moves = get_white_possible_moves(chess_board)
    filtered_moves = [move for moves in w_possible_moves for move in moves]
    castle_squares = [[0, 4], [0, 5], [0, 6]]

    if chess_board[0][5] == 0 and chess_board[0][6] == 0:
        if all(square not in [[move[2], move[3]] for move in filtered_moves] for square in castle_squares):
            if b_king_not_moved:
                if chess_board[0][7] == 8:
                    if b_h_rook_not_moved:
                        return True

    return False


def long_castling_black(chess_board, king_x, king_y):
    w_possible_moves = get_white_possible_moves(chess_board)
    filtered_moves = [move for moves in w_possible_moves for move in moves]
    castle_squares = [[0, 4], [0, 3], [0, 2]]
    if chess_board[0][1] == 0 and chess_board[0][2] == 0 and chess_board[0][3] == 0:
        if all(square not in [[move[2], move[3]] for move in filtered_moves] for square in castle_squares):
            if b_king_not_moved:
                if chess_board[0][0] == 8:
                    if b_a_rook_not_moved:
                        return True

    return False

    # ----------------------------------------- Move Evaluation Algorythm -------------------------------


def prioritize_moves(moves, chess_board):
    capture_moves = []
    check_moves = []
    other_moves = []

    for move in moves:
        piece_captured = chess_board[move[2]][move[3]]
        if piece_captured != 0:
            capture_moves.append(move)
        elif is_king_in_check(simulate_move(chess_board, move), not is_white_turn):
            check_moves.append(move)
        else:
            other_moves.append(move)

    return capture_moves, check_moves, other_moves


def get_board_key(chess_board, is_white_turn):
    board_key = (tuple(tuple(row) for row in chess_board), is_white_turn)
    return board_key


def minimax(chess_board, depth, is_white_turn, alpha, beta, cache=None):
    if cache is None:
        cache = computed_moves_cache
    board_key = (get_board_key(chess_board, is_white_turn), depth)
    if board_key in computed_moves_cache:
        return cache[board_key]

    if depth == 0:
        game_state = is_check_mate(chess_board, is_white_turn)
        if game_state == 'Checkmate':
            eval_score = (float('inf') if is_white_turn else float('-inf')) - depth
            cache[board_key] = eval_score
            return eval_score
        eval_score = evaluate_board_state(chess_board, is_white_turn)
        cache[board_key] = eval_score
        return eval_score

    game_state = is_check_mate(chess_board, is_white_turn)
    if game_state == 'Checkmate':
        eval_score = (float('inf') if is_white_turn else float('-inf')) - depth
        cache[board_key] = eval_score
        return eval_score
    elif game_state == 'Stalemate':
        eval_score = 0
        cache[board_key] = eval_score
        return eval_score

    if is_white_turn:
        max_eval = float('-inf')
        white_legal_moves = get_white_legal_moves(chess_board, is_white_turn)

        for move in white_legal_moves:
            temp_board = simulate_move(chess_board, move)

            eval = minimax(temp_board, depth - 1, False, alpha, beta, cache)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        cache[board_key] = max_eval
        return max_eval

    else:
        min_eval = float('inf')
        black_legal_moves = get_black_legal_moves(chess_board, is_white_turn)

        for move in black_legal_moves:
            temp_board = simulate_move(chess_board, move)

            eval = minimax(temp_board, depth - 1, True, alpha, beta, cache)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break

        cache[board_key] = min_eval
        return min_eval


def evaluate_board_state(chess_board, is_white_turn):
    piece_values = {1: 1, 2: 5, 3: 3, 4: 3, 5: 9, 6: 20, 7: -1, 8: -5, 9: -3, 10: -3, 11: -9, 12: -20}

    white_pawn_board_multiplier = [[8, 8, 8, 8, 8, 8, 8, 8],
                                   [1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6],
                                   [1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3],
                                   [1.1, 1.1, 1.1, 1.5, 1.5, 1.1, 1.1, 1.1],
                                   [1, 1, 1, 1.5, 1.5, 1, 1, 1],
                                   [0.9, 0.9, 0.9, 1.2, 1.2, 1, 1, 1.2],
                                   [0.8, 0.8, 0.8, 0.6, 0.6, 1.3, 1.3, 1.3],
                                   [1, 1, 1, 1, 1, 1, 1, 1]]

    black_pawn_board_multiplier = [[1, 1, 1, 1, 1, 1, 1, 1],
                                   [0.8, 0.8, 0.8, 0.6, 0.6, 1.3, 1.3, 1.3],
                                   [0.9, 0.9, 0.9, 1.2, 1.2, 1, 1, 1.2],
                                   [1, 1, 1, 1.5, 1.5, 1, 1, 1],
                                   [1.1, 1.1, 1.1, 1.5, 1.5, 1.1, 1.1, 1.1],
                                   [1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3],
                                   [1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6],
                                   [8, 8, 8, 8, 8, 8, 8, 8]]

    knight_board_multiplier = [[0.5, 0.9, 0.7, 0.7, 0.7, 0.7, 0.9, 0.5],
                               [0.6, 0.8, 0.9, 0.9, 0.9, 0.9, 0.8, 0.6],
                               [0.7, 0.9, 1.1, 1.1, 1.1, 1.1, 0.9, 0.7],
                               [0.7, 0.9, 1.1, 1.3, 1.3, 1.1, 0.9, 0.7],
                               [0.7, 0.9, 1.1, 1.3, 1.3, 1.1, 0.9, 0.7],
                               [0.7, 0.9, 1.1, 1.1, 1.1, 1.1, 0.9, 0.7],
                               [0.6, 0.8, 0.9, 0.9, 0.9, 0.9, 0.8, 0.6],
                               [0.5, 0.9, 0.7, 0.7, 0.7, 0.7, 0.9, 0.5]]

    bishop_board_multiplier = [[1, 1, 0.9, 1, 1, 0.9, 1, 1],
                               [1, 1.1, 1, 1, 1, 1, 1.1, 1],
                               [1, 1, 1, 1.1, 1.1, 1, 1, 1],
                               [1, 1.2, 1.2, 1.1, 1.1, 1.2, 1.2, 1],
                               [1, 1.2, 1.2, 1.1, 1.1, 1.2, 1.2, 1],
                               [1, 1, 1, 1.1, 1.1, 1, 1, 1],
                               [1, 1.1, 1, 1, 1, 1, 1.1, 1],
                               [1, 1, 0.9, 1, 1, 0.9, 1, 1]]

    rook_board_multiplier = [[1, 1, 1, 1.1, 1.1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1.1, 1.1, 1, 1, 1]]

    queen_board_multiplier = [[1, 1, 1, 0.95, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 0.95, 1, 1, 1, 1]]

    king_board_multiplier = [[1, 1, 1.02, 1, 1, 1, 1.04, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1.02, 1, 1, 1, 1.04, 1]]

    board_multiplier = {1: white_pawn_board_multiplier, 7: black_pawn_board_multiplier,
                        3: knight_board_multiplier, 9: knight_board_multiplier,
                        4: bishop_board_multiplier, 10: bishop_board_multiplier,
                        2: rook_board_multiplier, 8: rook_board_multiplier,
                        5: queen_board_multiplier, 11: queen_board_multiplier,
                        6: king_board_multiplier, 12: king_board_multiplier}

    if is_white_turn:
        game_state = is_check_mate(chess_board, is_white_turn)
        if game_state == 'Checkmate':
            return float('inf')
        if game_state == 'Stalemate':
            return 0
    else:
        game_state = is_check_mate(chess_board, is_white_turn)
        if game_state == 'Checkmate':
            return float('-inf')
        if game_state == 'Stalemate':
            return 0

    chess_board_state = 0

    for x in range(8):
        for y in range(8):
            piece = chess_board[x][y]
            if piece != 0:
                piece_value = piece_values.get(piece)
                chosen_multiplier = board_multiplier.get(piece)
                if chosen_multiplier:
                    position_multiplier = chosen_multiplier[x][y]

                    chess_board_state += piece_value * position_multiplier

    return chess_board_state


def find_best_move(chess_board, is_white_turn, depth, eval_diff=0.05):
    best_move = None
    top_moves = []
    alpha = float('-inf')
    beta = float('inf')
    global w_short_castle
    global w_long_castle
    global b_short_castle
    global b_long_castle

    if is_white_turn:
        max_eval = float('-inf')
        white_legal_moves = get_white_legal_moves(chess_board, is_white_turn)
        king_x, king_y = find_king(chess_board, 6)
        w_short_castle = short_castling_white(chess_board, king_x, king_y)
        w_long_castle = long_castling_white(chess_board, king_x, king_y)

        if w_short_castle:
            white_legal_moves.append([7, 4, 7, 6])
        if w_long_castle:
            white_legal_moves.append([7, 4, 7, 2])

        capture_moves, check_moves, other_moves = prioritize_moves(white_legal_moves, chess_board)
        prioritized_moves = check_moves + capture_moves + other_moves

        for move in check_moves:
            temp_board = simulate_move(chess_board, move)
            if is_check_mate(temp_board, is_white_turn):
                forced_mate_eval = minimax(temp_board, 3, not is_white_turn, alpha, beta)
                if forced_mate_eval == float('inf'):
                    return move

            eval = minimax(temp_board, depth - 1, not is_white_turn, alpha, beta)

            if eval > max_eval:
                max_eval = eval
                top_moves = [move]
                alpha = max(alpha, eval)

            if alpha >= beta:
                break

        for move in capture_moves:
            temp_board = simulate_move(chess_board, move)

            eval = minimax(temp_board, depth - 1, not is_white_turn, alpha, beta)

            if eval > max_eval:
                max_eval = eval
                top_moves = [move]
                alpha = max(alpha, eval)

            if alpha >= beta:
                break

        for move in other_moves:
            temp_board = simulate_move(chess_board, move)

            eval = minimax(temp_board, depth - 1, not is_white_turn, alpha, beta)

            if eval > max_eval:
                max_eval = eval
                top_moves = [move]
                alpha = max(alpha, eval)

            if alpha >= beta:
                break

    else:
        min_eval = float('inf')
        black_legal_moves = get_black_legal_moves(chess_board, is_white_turn)
        king_x, king_y = find_king(chess_board, 12)
        b_short_castle = short_castling_black(chess_board, king_x, king_y)
        b_long_castle = long_castling_black(chess_board, king_x, king_y)

        if b_short_castle:
            black_legal_moves.append([0, 4, 0, 6])
        if b_long_castle:
            black_legal_moves.append([0, 4, 0, 2])

        capture_moves, check_moves, other_moves = prioritize_moves(black_legal_moves, chess_board)
        prioritized_moves = check_moves + capture_moves + other_moves

        for move in check_moves:
            temp_board = simulate_move(chess_board, move)
            if is_check_mate(temp_board, is_white_turn):
                forced_mate_eval = minimax(temp_board, 3, not is_white_turn, alpha, beta)
                if forced_mate_eval == float('-inf'):
                    return move

            eval = minimax(temp_board, depth - 1, not is_white_turn, alpha, beta)

            if eval < min_eval:
                min_eval = eval
                top_moves = [move]
                beta = min(beta, eval)

            if alpha >= beta:
                break

        for move in capture_moves:
            temp_board = simulate_move(chess_board, move)

            eval = minimax(temp_board, depth - 1, not is_white_turn, alpha, beta)

            if eval < min_eval:
                min_eval = eval
                top_moves = [move]
                beta = min(beta, eval)

            if alpha >= beta:
                break

        for move in other_moves:
            temp_board = simulate_move(chess_board, move)

            eval = minimax(temp_board, depth - 1, not is_white_turn, alpha, beta)

            if eval < min_eval:
                min_eval = eval
                top_moves = [move]
                beta = min(beta, eval)

            if alpha >= beta:
                break

    if top_moves:
        print("roar", top_moves)
        best_move = random.choice(top_moves)
    else:
        if is_white_turn:
            moves = get_white_legal_moves(chess_board, True)
            if moves:
                best_move = random.choice(moves)
        else:
            moves = get_black_legal_moves(chess_board, False)
            if moves:
                best_move = random.choice(moves)

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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        visualize_game_state(screen)
        pygame.display.flip()

        if is_white_turn:
            start_time = time.perf_counter()
            print(" Its Whites turn!")
            if is_king_in_check(chess_board, is_white_turn):
                print(" White king is in check")
            if player_is_white:
                white_choice = get_player_move()
                if white_choice:
                    update_chess_board(chess_board, white_choice, is_white_turn)
                    visualize_game_state(screen)
                    pygame.display.flip()
                    game_state = is_check_mate(chess_board, is_white_turn)
                    if game_state == 'Checkmate':
                        print(" Checkmate for White!")
                        print("board eval", evaluate_board_state(chess_board, is_white_turn))
                        running = False
                        break
                    if game_state == 'Stalemate':
                        print(" Draw by Stalemate!")
                        print(" board eval", evaluate_board_state(chess_board, is_white_turn))
                        running = False
                        break

            else:
                best_move = find_best_move(chess_board, is_white_turn, depth)
                if best_move:
                    white_choice = best_move
                    piece_int = chess_board[white_choice[0]][white_choice[1]]
                    piece_str = w_piece_dict.get(piece_int)
                    print(f" White moves {piece_str} from "
                          f"{white_choice[0], white_choice[1]} to --> {white_choice[2], white_choice[3]}")
                    update_chess_board(chess_board, white_choice, is_white_turn)
                    visualize_game_state(screen)
                    pygame.display.flip()
                    board_eval = evaluate_board_state(chess_board, is_white_turn)
                    print(" Current state of the board:", board_eval)
                    if board_eval == float('inf'):
                        print(" Checkmate for White!")
                        running = False
                        break

                else:
                    print(" Draw by Stalemate")
                    running = False
                    break

            print(" Current state of the board:", evaluate_board_state(chess_board, is_white_turn))
            computed_moves_cache.clear()
            end_time = time.perf_counter()
            calc_time = end_time - start_time
            print(f"Move found after {calc_time:.4f} seconds")
            changing_turns()

        else:
            start_time = time.perf_counter()
            print(" It´s Blacks turn!")
            king_x, king_y = find_king(chess_board, 12)
            if is_king_in_check(chess_board, is_white_turn):
                print(" Black king is in check")
            if player_is_black:
                black_choice = get_player_move()
                if black_choice:
                    update_chess_board(chess_board, black_choice, is_white_turn)
                    visualize_game_state(screen)
                    pygame.display.flip()
                    game_state = is_check_mate(chess_board, is_white_turn)
                    if game_state == 'Checkmate':
                        print(" Checkmate for Black!")
                        running = False
                        break
                    if game_state == 'Stalemate':
                        print(" Draw by Stalemate!")
                        running = False
                        break

            else:
                best_move = find_best_move(chess_board, is_white_turn, depth)
                if best_move:
                    black_choice = best_move
                    piece_int = chess_board[black_choice[0]][black_choice[1]]
                    piece_str = b_piece_dict.get(piece_int)
                    print(f" Black moves {piece_str} from "
                          f"{black_choice[0], black_choice[1]} to --> {black_choice[2], black_choice[3]}")
                    update_chess_board(chess_board, black_choice, is_white_turn)
                    visualize_game_state(screen)
                    pygame.display.flip()
                    board_eval = evaluate_board_state(chess_board, is_white_turn)
                    print(" Current state of the board:", board_eval)
                    if board_eval == float('-inf'):
                        print(" Checkmate for Black!")
                        running = False
                        break
                else:
                    print(" Draw by Stalemate")
                    running = False
                    break

            print(" Current state of the board:", evaluate_board_state(chess_board, is_white_turn))
            computed_moves_cache.clear()
            end_time = time.perf_counter()
            calc_time = end_time - start_time
            print(f"Move found after {calc_time:.4f} seconds")
            changing_turns()

    pygame.quit()


def start_game():
    print("Choose game mode:")
    print("1. Play as White")
    print("2. Play as Black")
    print("3. AI vs AI")
    # print("4. Player vs Player")
    global player_is_white
    global player_is_black
    global ai_vs_ai
    game_mode = input("Enter 1, 2, 3: ")

    if game_mode not in ['1', '2', '3']:
        print("Invalid selection, Please enter 1, 2, 3")

    if game_mode == '1':
        player_is_white = True
    if game_mode == '2':
        player_is_black = True
    if game_mode == '3':
        ai_vs_ai = True

    precompute_white_pawn_moves()
    precompute_black_pawn_moves()
    precompute_knight_moves()
    precompute_horizontal_moves()
    precompute_vertical_moves()
    precompute_diagonal_moves()
    # precompute_king_moves()

    game_loop(screen, chess_board, depth)


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

    profiler = cProfile.Profile()
    profiler.enable()

    start_game()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('ncalls')
    stats.print_stats()
