count = 0
for i in range(12345678, 98765433):
    a = str(i).find('2')
    if a != -1:
        b = a + str(i)[a:].find('0')
        if b != a-1:
            c = b + str(i)[b:].find('2')
            if c != b-1:
                d = c + str(i)[c:].find('3')
                if d != c-1:
                    count += 1
print(98765433-12345678-count+1)