import random
import time


def my_square_and_multiply(num, e, N):
    operations = str(bin(e))[2:]
    mod_value = 1
    for op in operations:
        if op == "1":

            mod_value = (mod_value ** 2) * num
        else:
            mod_value **= 2
        if mod_value >= N:
            mod_value %= N
    return mod_value


def actual_square_and_multiply(num, e, N):
    operations = str(bin(e))[2:]
    mod_value = 1
    for op in operations:
        mod_value = mod_value ** 2
        mod_value %= N
        if op == "1":
            mod_value *= num
            mod_value %= N
    return mod_value



def counting_square_and_multiply(num, e, N):
    operations = str(bin(e))[2:]
    mod_value = 1
    count = 0
    for op in operations:
        mod_value = mod_value ** 2
        mod_value %= N
        if op == "1":
            if mod_value % 2 == 0:
                count += 1
            mod_value *= num
            mod_value %= N
    return count, mod_value


def timing_square_and_multiply(num, e, N):
    operations = str(bin(e))[2:]
    mod_value = 1
    for op in operations:
        mod_value = mod_value ** 2
        mod_value %= N
        if op == "1":
            if mod_value % 2 == 0:
                time.sleep(0.05)
            mod_value *= num
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
        encryptedMessage = actual_square_and_multiply(message, e, N)
        encrypted += chr(encryptedMessage)
    print(encrypted)
    print(f"Public Key = {hex(N)}, {bin(e)}")
    print(f"Private Key = {bin(d)}")
    return encrypted, d, N


def decrypt(text, d, N):
    listText = []
    decrypted = ""
    for letter in text:
        listText.append(ord(letter))
    for message in listText:
        decryptedMessage = my_square_and_multiply(message, d, N)
        decrypted += chr(decryptedMessage)
    print(decrypted)


def proper_decrypt():
    publicKey = 0x81cb
    private = 0x34d9
    e = 0x11
    message = my_square_and_multiply(65, e, publicKey)
    print(private)
    decryptedMessage = my_square_and_multiply(message, private, publicKey)



# 0x4b73d755b10edcc3187779b905aec7a102b82e13ab084de7fed826698524e097
# 0x778db34bc38db694dfcaca7e60cb124711b5bc4db5f64808a544f82bc8b36c07
# 101000
# 0b10100000

#m, d, N = encrypt(input("Message = "))
#decrypt(m, d, N)

# proper_decrypt()

N = 0x778db34bc38db694dfcaca7e60cb124711b5bc4db5f64808a544f82bc8b36c07
e = 0x10001
message = 65
encrypted = my_square_and_multiply(message, e, N)

def please_work(d):
    decrypted = my_square_and_multiply(encrypted, d, N)
    if decrypted == 65:
        print(d)
        return True
    else:
        return False


def get_external_values():
    primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    p = random.choices(primes)[0]
    primes.remove(p)
    q = random.choices(primes)[0]
    N = p * q
    e, d = inverse_modulus(p, q)
    print(f"Correct: {bin(d)}")
    return N, d


# proper_decrypt()
