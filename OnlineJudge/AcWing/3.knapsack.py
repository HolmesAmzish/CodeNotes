n, max_weight = map(int, input().split())
items = []

for _ in range(n):
    weight, value = map(int, input().split())
    items.append((weight, value))

dp = [0] * (max_weight + 1)

for weight, value in items:
    for i in range(weight, max_weight + 1):
        dp[i] = max(dp[i], dp[i - weight] + value)

    print(dp)

print(dp[max_weight])

