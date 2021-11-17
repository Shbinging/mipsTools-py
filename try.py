def str2(n, m):
    if (n < 0):
        return str(bin(0xffffffff + n + 1)[2:]).zfill(m)
    return str(bin(n)[2:]).zfill(m)

c = -10
print(str2(-10, 32))
print(int("11111111111111111111111111110110", 2))
print(c >> 2)