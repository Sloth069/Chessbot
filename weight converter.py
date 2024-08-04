weight = input("weight: ")
Type = input("(k)g or (L)bs): ")

if Type == "K" :
    print("Your weight in pounds is", float(weight) * 2.205, "lb")
else :
    print("Your weight in kilograms is", float(weight) / 2.205, "kg")

print(type(weight))