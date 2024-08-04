"""
[X, 4, 3] [7, X, 9] [8, X, 6]
[X, 6, X] [5, X, X] [X, X, X]
[8, 2, X] [6, X, X] [4, 5, X]

[7, X, 4] [X, 8, X] [X, X, X]
[3, X, 9] [X, X, 2] [6, X, 5]
[X, X, X] [3, X, X] [X, 4, 1]

[6, X, X] [X, X, 4] [X, X, X]
[X, X, X] [8, 6, 7] [X, 9, X]
[4, 7, X] [X, X, 3] [5, 6, X]
"""

test = [[0, 4, 3], [7, 0, 9], [8, 0, 6],
        [0, 6, 0], [5, 0, 0], [0, 0, 0],
        [8, 2, 0], [6, 0, 0], [4, 5, 0]]


#for x in range(9):
    #for y in range(3):
       #print(test[x][y])



"""Algorythm:
1. Iterate over Sudoku_list where [x, y] = 0
2. Create List with elements 1-9
3. Erase elements from List that exist in "block"
4. Erase elements from list that exist in same row (modulo)
5. Erase elements from List that exist in same column
6. If len(List) == 1 then write the leftover number, 
    else move to next 0 
"""


# ----------------------------------------  Variables  ----------------------------------------------------

sudoku_list = [[0, 4, 3],[7, 0, 9],[8, 0, 6],
               [0, 6, 0],[5, 0, 0],[0, 0, 0],
               [8, 2, 0],[6, 0, 0],[4, 5, 0],

               [7, 0, 4],[0, 8, 0],[0, 0, 0],
               [3, 0, 9],[0, 0, 2],[6, 0, 5],
               [0, 0, 0],[3, 0, 0],[0, 4, 1],

               [6, 0, 0],[0, 0, 4],[0, 0, 0],
               [0, 0, 0],[8, 6, 7],[0, 9, 0],
               [4, 7, 0],[0, 0, 3],[5, 6, 0]]

element_list = []

# ----------------------------------------  1.  ----------------------------------------------------
# iterate over sudoku_list where [x, y] = 0
for x in range(27):
    for y in range(3):
        if sudoku_list[x][y] == 0:
            break


# ----------------------------------------  2.  ----------------------------------------------------

element_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ----------------------------------------  3.  ----------------------------------------------------

# ----------------------------------------  4.  ----------------------------------------------------
# Erase elements in List that exist in same row

def erase_row_numbers(x):
    x_start_value = x - (x % 3)
    y_start_value = 0
    for j in range(3):
        for k in range(3):
            number = sudoku_list[x_start_value + j][k]
            if number in element_list:
                element_list. remove(number)

erase_row_numbers(x, y)
print(element_list)

# ----------------------------------------  5.  ----------------------------------------------------
# erase elements in list that exist in same column


def erase_column_numbers(x, y):
    x_start_value = x % 3
    for j in range(9):
        number = sudoku_list[x_start_value + j * 3][y]
        if number in element_list:
            element_list.remove(number)


erase_column_numbers(x, y)
print(element_list)