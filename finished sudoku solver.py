"""
 X == 0
 | X[0, 0], 4[0, 1], 3[0, 2] | | 7[1, 0], X[1, 1], 9[1, 2] | | 8, X, 6 |
 | X[3, 0], 6[3, 1], X[3, 2] | | 5[4, 0], X[4, 1], X[4, 2] | | X, X, X |
 | 8[6, 0], 2[6, 1], X[6, 2] | | 6[7, 0], X[7, 1], X[7, 2] | | 4, 5, X |

 | 7[9, 0], X, 4 | | X, 8, X | | X, X, X|
 | 3, X[12, 1], 9 | | X, X, 2 | | 6, X, X|
 | X, X, X | | 3, X, X | | X, 4, 1|

 | 6, X, X | | X, X, 4 | | X, X, X|
 | X, X, X | | 8, 6, 7 | | X, 9, X|
 | 4, 7, X | | X, X, 3 | | 5, 6, X|

Ortbestimmung:
[x][y] = x blockspalte y = blockreihe von 3 x 3 Blöcken

(x / 3)abrunden % 3 --> elementspalte 0 oben | 1 mitte | 2 unten
y                   --> elementreihe 0 links | 1 mitte | 2 rechts

x[i] - 3 * [x] | y = 1 --> 4 * 2 | 1
[0,0][0,1][0,2]
[1,0][1,1][1,2]
[2,0][2,1][2,2]

[7, 2] --> 2, 2 --> [7] - 3 * [2] | 2
---> 7 - 6 | 2 - 2 ---> 1,0

[12, 1] --> 1, 1 --> [12] - 3 * [1] | 1
---> 12 - 3 | 1 - 1 ---> 9,0

Algo:
Algorythmus:
1. Iterate over Sudoku_list where [x, y] = 0
2. Create List with elements 1-9
3. Erase elements from List that exist in "block"
4. Erase elements from list that exist in same column
5. Erase elements from List that exist in same row
6. If len(List) == 1 then write the leftover number,
      else move to next 0
"""

# ------------------------------------------ Variables ------------------------------------------
"""
sudoku_list = [[0, 4, 3], [7, 0, 9], [8, 0, 6],
               [0, 6, 0], [5, 0, 0], [0, 0, 0],
               [8, 2, 0], [6, 0, 0], [4, 5, 0],

               [7, 0, 4], [0, 8, 0], [0, 0, 0],
               [3, 0, 9], [0, 0, 2], [6, 0, 0],
               [0, 0, 0], [3, 0, 0], [0, 4, 1],

               [6, 0, 0], [0, 0, 4], [0, 0, 0],
               [0, 0, 0], [8, 6, 7], [0, 9, 0],
               [4, 7, 0], [0, 0, 3], [5, 6, 0]]
"""

sudoku_list = [[4, 0, 5], [2, 0, 3], [8, 6, 0],
               [0, 0, 9], [0, 0, 8], [0, 0, 0],
               [8, 1, 0], [0, 4, 0], [0, 0, 0],

               [7, 0, 0], [8, 0, 0], [9, 0, 0],
               [0, 0, 1], [0, 0, 0], [4, 0, 0],
               [0, 0, 8], [0, 0, 5], [0, 0, 3],

               [0, 0, 0], [0, 7, 0], [0, 9, 6],
               [0, 0, 0], [6, 0, 0], [5, 0, 0],
               [6, 2, 0], [5, 3, 9], [1, 0, 8]]

element_list = []
counter = 0


# ------------------------------------------ 2. ------------------------------------------
# 2. Create List with elements 1-9
def create_element_list():
    global element_list
    element_list = [x for x in range(1, 10)]


# ------------------------------------------ 3. ------------------------------------------
# 3. Erase elements from List that exist in "block"
def erase_block_numbers(x, y):
    # 1. position bestimmen
    global element_list

    element_spalte = int((x / 3)) % 3
    topleft_x = x - (3 * element_spalte)
    topleft_y = 0

    # 1.2 über Elemente im Block iterieren
    for j in range(3):
        for k in range(3):
            number = sudoku_list[topleft_x + j * 3][topleft_y + k]
            if number in element_list:
                element_list.remove(number)


# ------------------------------------------ 4. ------------------------------------------
# 4. Erase elements from list that exist in same column
def erase_column_numbers(x, y):
    global element_list

    x_start_value = x % 3
    for j in range(9):
        number = sudoku_list[x_start_value + j * 3][y]
        if number in element_list:
            element_list.remove(number)


# ------------------------------------------ 5. ------------------------------------------
# 5. Erase elements from list that exist in same row
def erase_row_numbers(x, y):
    x_start_value = x - (x % 3)

    for j in range(3):
        for k in range(3):
            number = sudoku_list[x_start_value + j][k]
            if number in element_list:
                element_list.remove(number)


# ------------------------------------------  6.  --------------------------------------------
# If len(List) == 1 then write the leftover number, else move to next 0
def write_leftover_number(x, y):
    global counter

    if len(element_list) == 1 and len(element_list) > 0:
        sudoku_list[x][y] = element_list[0]
        print("Eindeutige Lösung", sudoku_list[x][y])
        counter = 0
    else:
        counter += 1


# ------------------------------------------  Extra  ------------------------------------------
def print_list():
    for j in range(9):
        print(sudoku_list[0 + j * 3:3 + j * 3])


# ------------------------------------------ 1. ------------------------------------------
# 1. Iterate over Sudokulist where [x, y] = 0
if __name__ == "__main__":

    while counter < 81:
        print("counter: ", counter)
        counter += 1
        for x in range(len(sudoku_list)):
            for y in range(len(sudoku_list[x])):
                if sudoku_list[x][y] == 0:
                    # 2. create list
                    create_element_list()

                    # 3.
                    erase_block_numbers(x, y)

                    # 4.
                    erase_column_numbers(x, y)

                    # 5.
                    erase_row_numbers(x, y)

                    # 6
                    write_leftover_number(x, y)

    print(print_list())
    print(sudoku_list[(1 + 3)][0])