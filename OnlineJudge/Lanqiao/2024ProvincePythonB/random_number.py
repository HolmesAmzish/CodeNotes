def power(base, exponent, modulus):
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def solve():
    length = 10000
    modulus = 10**9 + 7

    total = power(9, length, modulus)
    no_3 = power(8, length, modulus)
    no_7 = power(8, length, modulus)
    no_3_no_7 = power(7, length, modulus)

    result = (total - no_3 - no_7 + no_3_no_7) % modulus
    return result

print(solve())