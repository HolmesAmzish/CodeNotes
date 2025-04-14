import os
import sys

count = 0

for i_original in range(1, 2025):
    # Convert number to binary string by cutting prefix '0b'
    i = i_original
    binary_str = bin(i)[2:]
    binary_sum = sum(map(int, binary_str))

    quaternary_str = []
    i = i_original
    while i > 0:
        quaternary_str.append(str(i % 4))
        i //= 4

    quaternary_sum = sum(map(int, quaternary_str))

    count += 1 if binary_sum == quaternary_sum else 0

    # print(f"The binary sum is {binary_sum}, the quaternary sum is {quaternary_sum}")

print(count)