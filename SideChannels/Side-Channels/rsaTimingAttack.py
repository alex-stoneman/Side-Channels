import subprocess, time, math, random
import myRSA

# At the moment the challenge is set manually because I wasn't sure if I wanted to make
# p global or If I wanted to pass it thorough as a parameter like in errorMsg
chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
problem = "rsa-timing"
exe = f"./{problem}/oracle.windows"
p = subprocess.Popen(exe, stdin=subprocess.PIPE, stdout=subprocess.PIPE)


# test out a password and return the error message, ignore OS errors bc they were annoying
def interact(password):
    try:
        p.stdin.write(password.encode() + b'\n')
        p.stdin.flush()
        return p.stdout.readline().decode().strip()
    except OSError:
        print("BAD")

def time_test(test, d, N):
    first = time.perf_counter_ns()
    # interact(str(test))
    myRSA.timing_square_and_multiply(test, d, N)
    second = time.perf_counter_ns()
    diff = (second - first) / (10 ** 9)
    return round(diff, 5)


def count_test(test, d, N):
    return myRSA.counting_square_and_multiply(test, d, N)


def attack():
    private = 1
    N = 0xae9da269
    e = 0x11
    d = 0x522b4911

    encrypted = myRSA.actual_square_and_multiply(65, e, N)

    print(bin(d))
    maxLength = len(str(bin(N)))+ + 13
    noTests = 30
    repeat = 0
    reallyRepeat = 0
    # even, odd - longer, shorter
    while myRSA.actual_square_and_multiply(encrypted, private, N) != 65:
        times = [[0, 0], [0, 0]]
        while True:
            value = random.randint(1, 10000000000)
            previous, expected = count_test(value, private, N)
            expected = (expected ** 2) % N
            parity = expected % 2
            if times[parity][1] < noTests:
                times[parity][0] += time_test(value, d, N) - previous * 0.01
                times[parity][1] += 1
            elif parity == 0:
                if times[1][1] == noTests:
                    break
            elif times[0][1] == noTests:
                break
        longer = times[0][0] / noTests
        shorter = times[1][0] / noTests
        print(longer - shorter)
        time.sleep(1)
        if longer > shorter + 0.05:
            private = private * 2 + 1
            if repeat > 0:
                repeat -= 2
        elif longer < shorter + 0.02:
            private *= 2
            repeat += 1
        else:
            reallyRepeat += 1
            if reallyRepeat > 4:
                private //= 2
                reallyRepeat = 0
        if repeat > 6:
            while private % 2 == 0:
                private //= 2
            for x in range(3):
                private //= 2
            repeat //= 3
            if private == 0:
                private = 1

        if len(bin(private)) > maxLength:
            private //= 2 ** (maxLength // 2)

        print(bin(private))
        print(bin(d))
        print(repeat)
        print()

    print(private)


def test_the_water():
    pass


attack()
