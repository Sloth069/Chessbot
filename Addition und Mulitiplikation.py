

i = 1
while i < 6:
    i = i + 1

    value1 = input("Value 1: ")
    value2 = input("Value 2: ")

    if mode == "addition":
        sum = (float(value1) + float(value2))
        print(sum)
    else:
        sum = float(value1) * float(value2)
        print(sum)