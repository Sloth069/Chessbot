def hourglassSum(liste):

    biggest_sum = -100000

    for x in range(4):
        for y in range(4):

            hourglass = liste[x][y] + liste[x][y + 1] + liste[x][y + 2] + liste[x + 1][y + 1] + liste[x + 2][y] + \
                        liste[x + 2][y + 1] + liste[x + 2][y + 2]
            if biggest_sum < hourglass:
                biggest_sum = hourglass
    return biggest_sum

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    arr = []

    for _ in range(6):
        arr.append(list(map(int, input().rstrip().split())))

    result = hourglassSum(arr)

    fptr.write(str(result) + '\n')

    fptr.close()