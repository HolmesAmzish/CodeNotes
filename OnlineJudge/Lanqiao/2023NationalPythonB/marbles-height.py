#  1   4   10   20
#  + 3 + 6 + 10
# + 2 + 3 + 4

sum = 1
height = 1
add = 3
i = 2
while (sum <= 20230610):
    sum += add
    i += 1
    add += i
    height += 1
print(sum)
print(height)

