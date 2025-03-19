n, max_weight = map(int, input().split())
items = []

for _ in range(n):
    weight, value, count = map(int, input().split())
    items.append((weight, value, count))

dp = [0] * (max_weight + 1)

for weight, value, count in items:
    for i in range(max_weight, weight - 1, -1):
        for j in range(1, min(i // weight, count) + 1):
            dp[i] = max(dp[i], dp[i - j * weight] + j * value)

print(dp[max_weight])