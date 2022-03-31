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


# Successful for 32 bit primes using 80 tests
# Gonna test 128 bit primes using 200 tests
def attack():
    totalTimeStart = time.perf_counter_ns()
    private = 1
    N = 0xf32c0b00906a9bab
    e = 0x10001
    d = 0x6ddafcd08ff9b621
    print(bin(d))
    expectedTimeDifference = 0.01
    encrypted = myRSA.actual_square_and_multiply(65, e, N)
    repeatedZeroLimit = int(len(bin(N)) // 8.5)
    maxLength = len(str(bin(N))) + 20
    noTests = 200
    repeat = 0
    reallyRepeat = 0
    # even, odd - longer, shorter
    while myRSA.actual_square_and_multiply(encrypted, private, N) != 65:
        times = [[0, 0], [0, 0]]
        if myRSA.actual_square_and_multiply(encrypted, 2 * private + 1, N) == 65:
            print(private * 2 + 1)
            break
        elif myRSA.actual_square_and_multiply(encrypted, 2 * private, N) == 65:
            print(private * 2)
            break
        while True:
            value = random.randint(1, 10000000000)
            previous, expected = count_test(value, private, N)
            expected = (expected ** 2) % N
            parity = expected % 2
            if times[parity][1] < noTests:
                times[parity][0] += time_test(value, d, N) - previous * expectedTimeDifference
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
        if shorter + 10 * expectedTimeDifference > longer > shorter + expectedTimeDifference:
            private = private * 2 + 1
            if repeat > 1:
                repeat -= 2
            elif repeat == 1:
                repeat = 0
        elif longer < shorter + (3 / 5) * expectedTimeDifference or abs(longer - shorter) > 25 * expectedTimeDifference:
            private *= 2
            repeat += 1
        else:
            reallyRepeat += 1
            if reallyRepeat > 4:
                private //= 2
                reallyRepeat = 0
        if repeat > repeatedZeroLimit:
            for x in range(repeatedZeroLimit + 6):
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

    print(bin(private))
    totalTimeFinish = time.perf_counter_ns()
    print(f"{(totalTimeFinish - totalTimeStart) // (10 ** 9)}s")


def test_the_water():
    pass


attack()
