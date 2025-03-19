from collections import deque

n, max_weight = map(int, input().split())
items = []

for _ in range(n):
    weight, value, count = map(int, input().split())
    items.append((weight, value, count))

dp = [0] * (max_weight + 1)

for weight, value, count in items:
    for mod in range(weight):
        # 单调队列初始化
        q = deque()
        # 遍历组内元素：i = mod + k * weight
        for k in range((max_weight - mod) // weight + 1):
            i = k * weight + mod
            val = dp[i] - k * value

            # 弹出队尾不优的元素
            while q and val >= dp[q[-1]] - ((q[-1] - mod) // weight) * value:
                q.pop()
            q.append(i)

            # 队首不满足约束，超出允许个数范围，弹出
            while q and k - ((q[0] - mod) // weight) > count:
                q.popleft()

            # 取队首进行更新
            dp[i] = dp[q[0]] + (k - ((q[0] - mod) // weight)) * value

print(dp[max_weight])
