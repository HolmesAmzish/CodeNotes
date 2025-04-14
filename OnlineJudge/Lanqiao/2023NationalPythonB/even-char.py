string = input()

letter_count = {}
for char in string.lower():
    letter_count[char] = letter_count.get(char, 0) + 1

flag = True
for _, count in letter_count.items():
    if count % 2 != 0:
        flag = False
        break

print("YES" if flag else "NO")