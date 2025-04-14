def get_fibonacci(index):
    if index == 1 or index == 2:
        return 1
    else:
        return get_fibonacci(index - 1) + get_fibonacci(index - 2)
    
for i in range(1, 100):
    print(f"{get_fibonacci(i):}")