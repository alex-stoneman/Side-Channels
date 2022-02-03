from time import sleep
import argparse

# 0x values are Hexadecimal
#
# N = 0x778db34bc38db694dfcaca7e60cb124711b5bc4db5f64808a544f82bc8b36c07
# Public exponent:
N = 0x81cb
e = 0x10001
d = 0x101000


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-mod', default='', const='', nargs='?', 
                        help='Modulus to be used, in hex')
    parser.add_argument('-priv', default='',const='', nargs='?', 
                        help='Private exponent to be used, in hex')
    args = parser.parse_args()

    try:
        args.mod = int(args.mod, 16)
        if args.mod != 0:
            mod_success = True
        else:
            mod_success = False
    except:
        args.mod = 0
        mod_success = False

    try:
        args.priv = int(args.priv, 16)
        if args.priv != 0:
            priv_success = True
        else:
            priv_success = False
    except:
        args.priv = 0
        priv_success = False

    if priv_success != mod_success:
        print("If a modulus is provided a private exponent must be too, and vice versa\n")
        parser.print_help()
        return args, False       

    return args, True


def main():
    args, ok = parse_args()
    if not ok:
        exit()

    if args.mod != 0:
        modulus = args.mod
    else:
        modulus = N

    if args.priv != 0:
        priv_exp = args.priv
    else:
        priv_exp = d

    while True:
        ct = input()

        try:
            c = int(ct, 16)
        except:
            print("Invalid hex ciphertext.")
            exit()

        m = pow_mod(c, priv_exp, modulus)
        print(f"Done: {m}")
        print(c)
        print(priv_exp)
        print(modulus)


def pow_mod(x, d, N):
    m = 1
    print(f"d = {d}")
    i = len(str(bin(d))) - 1
    while i >= 0:
        m = m * m
        m = m % N
        if d >> i == 1:
            m = multiply(m, x)
            m = m % N
        i = i - 1

    return m


def multiply(a, b):
    if get_bit(a, 0) == 0:
        # I've got a great idea for a quicker way to multiply
        # when this is true! I haven't actually timed it, but I'm
        # sure it'll be loads better!
        return my_better_multiply(a,b)
    else:
        return a*b

def get_bit(x, i):
    return (x >> i) & 1


def my_better_multiply(a, b):
    # What a genius! Bitshifting like this must make things so much faster
    # because we multiply much smaller numbers.
    a = a>>1
    result = a * b
    result = result<<1

    # turns out it's not when you only do one bit
    sleep(0.001)
    return result

main()
