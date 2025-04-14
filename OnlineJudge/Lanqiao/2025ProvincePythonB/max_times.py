word_list = ['lqb', 'lbq;', 'blq', 'bql', 'qlb', 'qbl']
word = input()

count = 0
index = 0
while index < len(word):
    # print(f"index: {index}, word[index: index + 3]: {word[index: index + 3]}")
    if word[index: index + 3] in word_list:
        count += 1
        index += 3
    else:
        index += 1

print(count)