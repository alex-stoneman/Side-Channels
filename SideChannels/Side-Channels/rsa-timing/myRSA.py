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
                time.sleep(0.01)
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



def encrypt(text):
    primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    p = random.choices(primes)[0]
    primes.remove(p)
    q = random.choices(primes)[0]
    N = p * q
    e, d = inverse_modulus(p, q)
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


def hex_to_string(hexString):
    letters = ""
    currentAscii = ""
    for character in hexString:
        currentAscii += character
        if int(currentAscii, 16) > 128:
            letters += chr(int(currentAscii[:-1], 16))
            currentAscii = character
    letters += chr(int(currentAscii, 16))
    print(letters, end="")


def decrypt_file():
    publicKey = 0x778db34bc38db694dfcaca7e60cb124711b5bc4db5f64808a544f82bc8b36c07
    private = 0x5ebe0cb89de05030eaa8ea8ffc64f1b608e959a8d800222ea9c1e4c3febad71
    file = open("ciphertext.txt", "r")
    hiddenMessage = ""
    for line in file:
        message = int(line, 16)
        decryptedMessage = actual_square_and_multiply(message, private, publicKey)
        hiddenMessage = ""
        hex_to_string(str(hex(decryptedMessage))[2:])


def get_external_values():
    primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    p = random.choices(primes)[0]
    primes.remove(p)
    q = random.choices(primes)[0]
    N = p * q
    e, d = inverse_modulus(p, q)
    print(f"Correct: {bin(d)}")
    return N, d


# decrypt_file()
# hex_to_string("35CE2753B0D8D653B52D56A855782017")
print(len(str(bin(0x778db34bc38db694dfcaca7e60cb124711b5bc4db5f64808a544f82bc8b36c07))) - 2)