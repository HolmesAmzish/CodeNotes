n = int(input())
number = list(map(int, input().split()))
sum = 0
for i in range(n):
    for j in range(i + 1, n):
        sum += (number[i] ^ number[j]) * (j - i)
print(sum)