n = int(input())
m = int(input())

# 预计算数位和
def digit_sum(x):
    return sum(int(d) for d in str(x))

# 生成1到n的列表，并附带数位和
numbers = list(range(1, n + 1))
# 按数位和升序，数值升序排序
numbers.sort(key=lambda x: (digit_sum(x), x))

# 输出第m个元素（注意列表是0-based）
print(numbers[m - 1])