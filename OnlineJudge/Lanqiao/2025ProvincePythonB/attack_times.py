HP = 2025
i = 1
while (HP > 0):
    first = 5
    second = 15 if i % 2 ==1 else 2
    if i % 3 == 1:
        third = 3
    elif i % 3 == 2:
        third = 10
    else:
        third = 7
    HP -= first + second + third
    i += 1
    print(HP)

print(i - 1)