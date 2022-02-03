def pow_mod(x, d, N):
    m = 1
    print(f"d = {d}")
    i = len(str(bin(d))) - 1
    while i >= 0:
        m = m * m
        m = m % N
        if d >> i == 1:
            m = m * x
            m = m % N
        i = i - 1

    return m