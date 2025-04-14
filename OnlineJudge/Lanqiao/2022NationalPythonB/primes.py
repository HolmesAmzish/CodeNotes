from math import *


def isPrime(n):
    for i in range(2, int(sqrt(n))+1):
        if n % i == 0:
            return False
    return True


dic = {}
with open('primes.txt', 'r') as file:
    txt = file.readlines()

cnt = 0
for num in txt:
    num = int(num[:-1])
    if num in dic:
        if dic[num]:
            cnt += 1
    else:
        if isPrime(num):
            cnt += 1
            dic[num] = True
        else:
            dic[num] = False
        tmp = num*2
        while tmp <= 10**8:
            dic[tmp] = False
            tmp += num


print(cnt)
print('end')
# 342693

