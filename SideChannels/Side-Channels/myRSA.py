import random
import time

# Finish
# Priority 1
def square_and_multiply(num, e, N):
    operations = str(bin(e))[2:]
    print(operations)


def prime_factorise(a):
    b = 2
    factors = []
    while b < a + 1:
        if a / b == a // b:
            a //= b
            factors.append(b)
        else:
            b += 1
    return factors


def greatest_common_divisor(a, b):
    listA = prime_factorise(a)
    listB = prime_factorise(b)
    temp = 1
    for item in listA:
        if item in listB:
            temp *= item
            listB.remove(item)
    return temp


# Finish
# Priority 2
def inverse_modulous():
    pass
def main():
    plain = input(": ")
    plainList = []
    for character in plain:
        plainList.append(ord(character))
    print(plainList)
    N = 0xf32c0b00906a9bab
    e = 0x10001
    d = 0x6ddafcd08ff9b621

    encrypted = []
    for item in plainList:
        newVal = (item ** e) % N
        encrypted.append(newVal)
    print(encrypted)

    final = []
    for item in encrypted:
        newVal = (item ** d) % N
        final.append(newVal)

    print(final)



'''
primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
p = random.choice(primes)
q = p
while q == p:
    q = random.choice(primes)
h = ((p - 1) * (q - 1)) // greatest_common_divisor(p - 1, q - 1)
print(p)
print(q)
print(h)
while True:
    e = random.randint(2, h - 1)
    if greatest_common_divisor(e, h) == 1:
        break
print(e)
'''