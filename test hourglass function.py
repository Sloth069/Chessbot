liste = [[1, 1, 1, 0, 0, 0],
        [1, 0, 0, 1, 0, 1],
        [1, 1, 0, 1, 1, 1],
        [0, 1, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 1],
        [0, 1, 0, 0, 1, 1]]


biggest_sum = liste[0][0]


for x in range(4):
    for y in range(4):

        hourglass = liste[x][y] + liste[x][y+1] + liste[x][y+2] + liste[x+1][y+1] + liste[x+2][y] + liste[x+2][y+1] + liste[x+2][y+2]
        if biggest_sum < hourglass:
            biggest_sum = hourglass
print(biggest_sum)





