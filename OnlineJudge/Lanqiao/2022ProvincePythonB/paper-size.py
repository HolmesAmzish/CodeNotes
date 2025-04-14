size_list = []
base_length = 1189
base_width = 841
for i in range(0, 10):
    size_list.append((base_length, base_width))
    base_length, base_width = base_width, base_length // 2

paper = {
    'A0': size_list[0],
    'A1': size_list[1],
    'A2': size_list[2],
    'A3': size_list[3],
    'A4': size_list[4],
    'A5': size_list[5],
    'A6': size_list[6],
    'A7': size_list[7],
    'A8': size_list[8],
    'A9': size_list[9]
}

input = input()
length, width = paper[input]
print(f'{length}\n{width}')