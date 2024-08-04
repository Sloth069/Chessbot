xFib = int(input("Eingabe: "))

v1 = 0
v2 = 1
i = 0

''' 
if xFib == 1:
    print("Fibonacci Sequenz bis", xFib)
else:
    for i in range(0,xFib):
        sum = v1 + v2
        v1 = v2
        v2 = sum
        print(sum)
'''
for i in range(0,xFib):
    sum = v1 + v2
    v1 = v2
    v2 = sum
    if i is xFib - 1:
        print(sum)
