n, m = map(int, input().split())
grid = []
for _ in range(n):
    grid.append(list(map(int, input().split())))

value_positions = {}
for a in range(n):
    for b in range(m):
        value = grid[a][b]
        if value not in value_positions:
            value_positions[value] = []
        value_positions[value].append((a, b))

count = 0
for value, positions in value_positions.items():
    for i in range(len(positions)):
        for j in range(len(positions)):
            a, b = positions[i]
            c, d = positions[j]
            if abs(a - c) == abs(b - d) > 0:
                count += 1
                # print(f"({a + 1}, {b + 1}) and ({c + 1}, {d + 1})")

print(count)