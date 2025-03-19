n, max_weight = map(int, input().split())
items = []

for _ in range(n):
    weight, value, count = map(int, input().split())
    items.append((weight, value, count))

# Pack items
packed_items = []
for weight, value, count in items:
    k = 0
    while count - 2**k >= 0:
        packed_weight = weight * 2**k
        packed_value = value * 2**k
        packed_items.append((packed_weight, packed_value))
        count -= 2**k
        k += 1
    packed_items.append((weight * count, value * count))

# Convert to 0-1 knapsack problem
dp = [0] * (max_weight + 1)
for weight, value in packed_items:
    for i in range(max_weight, weight - 1, -1):
        dp[i] = max(dp[i], dp[i - weight] + value)

print(dp[max_weight])