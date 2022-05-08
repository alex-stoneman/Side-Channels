import matplotlib.pyplot as plt
import time


def prime_factorise(a):
    b = 2
    factors = []
    prev = True
    while b < a + 1:
        if a / b == a // b:
            if prev:
                return 0
            a //= b
            factors.append(b)
            prev = True
        else:
            prev = False
            b += 1
    if len(factors) % 2 == 0:
        return 1
    else:
        return -1

first = time.perf_counter_ns()
values = []
total = 0
for x in range(int(input(": "))):
    total += prime_factorise(x)
    values.append(total)
second = time.perf_counter_ns()
diff = (second - first) / (10 ** 9)
print(f"{diff}s")
# print(values)

plt.plot(values)
plt.title("Merten's Conjecture")
plt.ylabel("Sum of values")
plt.xlabel("n")
plt.show()