t = int(input())

while (t):
    flag = False
    n, m = map(int, input().split())
    mod_dict = {}
    for i in range(1, m + 1):
        mod_dict[n % i] = mod_dict.get(n % i, 0) + 1
        if mod_dict[n % i] > 1:
            flag = True
            break
    print("Yes" if flag else "No")
    

    t -= 1