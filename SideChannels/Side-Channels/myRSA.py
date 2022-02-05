import random
import time


def square_and_multiply(num, e, N):
    operations = str(bin(e))[3:]
    mod_value = num % N
    for op in operations:
        if op == "1":
            mod_value = (mod_value ** 2) * num
        else:
            mod_value **= 2
        if mod_value >= N:
            mod_value %= N
    return mod_value


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



def inverse_modulus(p, q):
    funkyMod = abs((p - 1) * (q - 1)) // greatest_common_divisor(p - 1, q - 1)
    while True:
        e = random.randint(2, funkyMod - 1)
        if greatest_common_divisor(e, funkyMod) == 1:
            break
    while True:
        d = random.randint(100, 1000000)
        if (d * e) % funkyMod == 1:
            return e, d


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


def encrypt(text):
    primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    p = random.choices(primes)[0]
    primes.remove(p)
    q = random.choices(primes)[0]
    N = p * q
    #N = 0x778db34bc38db694dfcaca7e60cb124711b5bc4db5f64808a544f82bc8b36c07
    e, d = inverse_modulus(p, q)
    #e = 0b10001
    #d = 0b101000
    listText = []
    encrypted = ""
    for letter in text:
        listText.append(ord(letter))
    for message in listText:
        encryptedMessage = square_and_multiply(message, e, N)
        encrypted += chr(encryptedMessage)
    print(encrypted)
    print(f"Public Key = {N}, {e}")
    print(f"Private Key = {d}")


def decrypt(text):
    d = int(input("Private key = "), 16)
    N = int(input("Public key Mod = "))
    listText = []
    decrypted = ""
    for letter in text:
        listText.append(ord(letter))
    print(decrypted)


def proper_decrypt():
    message = 0x4b73d755b10edcc3187779b905aec7a102b82e13ab084de7fed826698524e097
    publicKey = 0x778db34bc38db694dfcaca7e60cb124711b5bc4db5f64808a544f82bc8b36c07
    private = int(input("Private: "), 2)
    private = 1052672
    print(private)
    decryptedMessage = square_and_multiply(message, private, publicKey)
    print(decryptedMessage)
    print(publicKey)
    print(chr(decryptedMessage))

# 0x4b73d755b10edcc3187779b905aec7a102b82e13ab084de7fed826698524e097
# 0x778db34bc38db694dfcaca7e60cb124711b5bc4db5f64808a544f82bc8b36c07
# 101000
# 0b10100000


# encrypt(input("Message = "))
# decrypt(input("CypherText ="))
# proper_decrypt()