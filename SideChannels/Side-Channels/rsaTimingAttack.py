import subprocess, time, random, operator
import myRSA
from matplotlib import pyplot as plt

# At the moment the challenge is set manually because I wasn't sure if I wanted to make
# p global or If I wanted to pass it thorough as a parameter like in errorMsg
chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
problem = "rsa-timing"
exe = f"./{problem}/oracle.windows"
p = subprocess.Popen(exe, stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def wipe_file():
    file = open("recordedTiming.txt", "w")
    file.write("0.01,1\n")
    file.close()


def record_result(result, position):
    file = open("recordedTiming.txt", "a")
    file.write(f"{result},{position}\n")
    file.close()


def plot_results(length):
    results = [[], []]
    positions = [[], []]
    finalDecision = []
    listOfTimes = []
    file = open("recordedTiming.txt", "r")
    for line in file:
        listOfTimes.append(line.split(","))
    file.close()

    for items in listOfTimes[::-1]:
        # mark the final decision for a bit in red and failed attempts in blue
        if items[1] in finalDecision:
            results[1].append(float(items[0]))
            positions[1].append(float(items[1]))
        else:
            finalDecision.append(items[1])
            results[0].append(float(items[0]))
            positions[0].append(int(items[1]))
    plt.plot(results[1], positions[1], "bo", label="Unused Results")
    plt.plot(results[0], positions[0], "or", label="Used Results")
    plt.vlines(0.04, 0, length, "g", label="Certainty Regions")
    plt.vlines(0.0075, 0, length, "g")
    plt.vlines(0.01, 0, length, "g")
    plt.legend()
    plt.xlabel("Average time Difference")
    plt.ylabel("Bit number")
    yInt = []
    for x in range(length + 2):
        yInt.append(x)
    plt.yticks(yInt)
    plt.show()


def which_key():
    file = open("test-numbers.txt", "r")
    count = 1
    values = []
    for line in file:
        whereInFile = (count - 3) % 6
        if whereInFile in [0, 1, 2]:
            #print(line)
            a, b = line.split(" = ")
            if whereInFile == 0:
                values.append([])
            values[-1].append(int(b[2:-1], 16))
        count += 1
    print(values)
    print("1: 8 bit primes")
    print("2: 16 bit primes")
    print("3: 32 bit primes")
    print("4: 64 bit primes")
    print("5: 128 bit primes")
    while True:
        choice = int(input(": "))
        if choice in [1, 2, 3, 4, 5]:
            returnValues = values[choice - 1]
            return returnValues[0], returnValues[1], returnValues[2]


# test out a password and return the error message, ignore OS errors bc they were annoying
def interact(password):
    try:
        p.stdin.write(password.encode() + b'\n')
        p.stdin.flush()
        return p.stdout.readline().decode().strip()
    except OSError:
        print("BAD")


def time_practise_test(test, d, N):
    first = time.perf_counter_ns()
    myRSA.timing_square_and_multiply(test, d, N)
    second = time.perf_counter_ns()
    diff = (second - first) / (10 ** 9)
    return round(diff, 5)


def time_test(test):
    first = time.perf_counter_ns()
    interact(test)
    second = time.perf_counter_ns()
    diff = (second - first) / (10 ** 9)
    return round(diff, 5)


def count_test(test, d, N):
    return myRSA.counting_square_and_multiply(test, d, N)


# Successful for 32 bit primes using 80 tests
# I'm going to test 128 bit primes using 200 tests
def practice_attack():
    N, e, d = which_key()
    totalTimeStart = time.perf_counter_ns()
    private = 1
    expectedTimeDifference = 0.01
    encrypted = myRSA.actual_square_and_multiply(65, e, N)
    repeatedZeroLimit = int(len(bin(N)) // 8.5) + 4
    maxLength = len(str(bin(N))) + 20
    noTests = 160
    repeat = 0
    reallyRepeat = 0
    # even, odd - longer, shorter
    while myRSA.actual_square_and_multiply(encrypted, private, N) != 65:
        times = [[0, 0], [0, 0]]
        if myRSA.actual_square_and_multiply(encrypted, 2 * private + 1, N) == 65:
            private = private * 2 + 1
            record_result(0.01, len(str(bin(private))) - 2)
            break
        elif myRSA.actual_square_and_multiply(encrypted, 2 * private, N) == 65:
            private = private * 2
            record_result(0, len(str(bin(private))) - 2)
            break
        while True:
            value = random.randint(1, 10000000000)
            previous, expected = count_test(value, private, N)
            expected = (expected ** 2) % N
            parity = expected % 2
            if times[parity][1] < noTests:
                times[parity][0] += time_practise_test(value, d, N) - previous * expectedTimeDifference
                times[parity][1] += 1
            elif parity == 0:
                if times[1][1] == noTests:
                    break
            elif times[0][1] == noTests:
                break
        longer = times[0][0] / noTests
        shorter = times[1][0] / noTests
        print(longer - shorter)
        if 4 * expectedTimeDifference > longer - shorter > expectedTimeDifference:
            private = private * 2 + 1
            if repeat > 1:
                repeat -= 2
            elif repeat == 1:
                repeat = 0
            record_result(round(longer - shorter, 6), len(str(bin(private))) - 2)
        elif longer < shorter + 0.75 * expectedTimeDifference:
            private *= 2
            repeat += 1
            record_result(round(longer - shorter, 6), len(str(bin(private))) - 2)
        else:
            reallyRepeat += 1
            if reallyRepeat > 4 or abs(longer - shorter) > 25 * expectedTimeDifference:
                private //= 2
                reallyRepeat = 0
            record_result(round(longer - shorter, 6), len(str(bin(private))) - 1)
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
        print(reallyRepeat)
        print()

    print(bin(private))
    totalTimeFinish = time.perf_counter_ns()
    print(f"total time = {(totalTimeFinish - totalTimeStart) // (10 ** 9)}s")
    plot_results(len(str(bin(d))) - 2)


def attack():
    N = 0x778db34bc38db694dfcaca7e60cb124711b5bc4db5f64808a544f82bc8b36c07
    e = 0x10001
    totalTimeStart = time.perf_counter_ns()
    private = 1


    expectedTimeDifference = 0.01
    encrypted = myRSA.actual_square_and_multiply(65, e, N)
    repeatedZeroLimit = int(len(bin(N)) // 8.5) + 4
    maxLength = len(str(bin(N))) + 20
    noTests = 100
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
                test = str(hex(value))
                test2 = test[2:]
                times[parity][0] += time_test(test2) - previous * expectedTimeDifference
                times[parity][1] += 1
            elif parity == 0:
                if times[1][1] == noTests:
                    break
            elif times[0][1] == noTests:
                break
        longer = times[0][0] / noTests
        shorter = times[1][0] / noTests
        print(longer - shorter)
        if shorter + 10 * expectedTimeDifference > longer > shorter + expectedTimeDifference:
            private = private * 2 + 1
            if repeat > 1:
                repeat -= 2
            elif repeat == 1:
                repeat = 0
        elif longer < shorter + 0.6 * expectedTimeDifference:
            private *= 2
            repeat += 1
        else:
            reallyRepeat += 1
            if reallyRepeat > 4 or abs(longer - shorter) > 25 * expectedTimeDifference:
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
        print(repeat)
        print()

    print(bin(private))
    totalTimeFinish = time.perf_counter_ns()
    print(f"total time = {(totalTimeFinish - totalTimeStart) // (10 ** 9)}s")


def check_for_repeated_key(tests):
    # [key, no.repetitions]
    repeats = {}
    for item in tests:
        if item in repeats:
            repeats[item] += 1
        else:
            repeats[item] = 1
    print(repeats)
    sortedRepeats = sorted(repeats.items(), key=operator.itemgetter(1))
    print(sortedRepeats)
    # At least 3 times, some certainty
    if sortedRepeats[0][1] >= 3:
        if len(sortedRepeats) > 1:
            # Must be a distinguishable preference
            if sortedRepeats[0][1] > sortedRepeats[1][1] + 1:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def attack_in_8_bits():
    totalTimeStart = time.perf_counter_ns()
    private = 1
    N = 0x81cb
    e = 0x11
    d = 0x34d9
    print(bin(d))

    expectedTimeDifference = 0.01
    encrypted = myRSA.actual_square_and_multiply(65, e, N)
    noTests = int(1.6 * len(bin(N)))
    count = 0
    currentTests = []
    reallyRepeat = 0
    # even, odd - longer, shorter
    while myRSA.actual_square_and_multiply(encrypted, private, N) != 65:
        if count == 8:
            currentTests.append(private)
            check = check_for_repeated_key(currentTests)
            # Only the current key can ever be accepted
            if check:
                currentTests = []
            else:
                print("HERE")
                private >>= 8
                print(private)
                if private <= 1:
                    private = 1
            count = 0
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
                # times[parity][0] += time_practise_test(value, d, N)
                test = str(hex(value))
                test2 = test[2:]
                times[parity][0] += time_test(test2) - previous * expectedTimeDifference
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
        elif longer < shorter + (3 / 5) * expectedTimeDifference:
            private *= 2
        else:
            reallyRepeat += 1
            if reallyRepeat > 4 or abs(longer - shorter) > 50 * expectedTimeDifference:
                private //= 2
                reallyRepeat = 0
                count -= 1

        print(bin(private))
        # print(bin(d))

        count += 1
        print(count)
        print()

    print(bin(private))
    totalTimeFinish = time.perf_counter_ns()
    print(f"total time = {(totalTimeFinish - totalTimeStart) // (10 ** 9)}s")


# attack_in_8_bits()
wipe_file()
practice_attack()
# plot_results(15)


# N = 0b111011110001101101100110100101111000011100011011011011010010100110111111100101011001010011111100110000011001011000100100100011100010001101101011011110001001101101101011111011001001000000010001010010101000100111110000010101111001000101100110110110000000111


# 1st
# 0b11110000101001010100000000101100011100001000000010000111000100000001100111010010010000010000110001000001000010110011001011000110010000111101010000001111000011000001001000001000011100000000100010000010001010101111011000000100100000110001101111001100110001101011110011100001110
# 0b11110000101001010100000000101100011100001000000010000111000100000001100111010010010000010000110001000001000010110011001011000110010000111100010000001001101010010100110100001100101001000100000101111011001100101010000000000111011010111100010000100010011111001100101100000001101
# 0b11110000101001010100000000101100011100001000000010000111000100000001100111010010010000010000110001000001000010110011001011000110010000111100000110000100010011010011110000000111010110100100101001000010001000001000101001010010110110000010000001101110001100100100111001100101001
# 0b111100001010010101000000001011000111000010000000100001110001000000011001110100100100000100001100010000010000101100110010110001100100001111110000100100010000100011000001000001010111010011011000110010001100100001001011100000101001
# 2

# Fairly damn confident in this: - less so now
# 0b111010010100100100010100100000011110101101000000011101010010010000100110001010111001100110101100001100001110001100000110000010101000101010

# 0b11101001010010010001010010000001111010110100000001110101001001000010011000101011100110011010110000110000111000110000011000001010100010101001010011010001100001010001111110010101100000100001001011011010101000100001110001001001111100001000000000101001010100010101001
# 0b11101001010010010001010010000001111010110100000001110101001001000010011000101011100110011010110000110000111000110000011000001010100010101010100011100011101000101010001000010000000100101010100011000001011010100001110001010010100000101011001011010000001000100110000110000000100
# 0b11101001010010010001010010000001111010110100000001110101001001000010011000101011100110011010110000110000111000110000011000001010100010101000101001000001000010010010000000100001101111101010011101000101000010000001100100100011101010100000101001000000010000001100101010000100100
# 0b11101001010010010001010010000001111010110100000001110101001001000010011000101011100110011010110000110000111000110000011000001010100010101000110111010000000000000100010010000000100010100111001100010001011101011000010100000100000001110000000001011001100000100000110001111001111
#


# who knows
# 0b1100100101001001010001001000000000001110000010100001100001000000010001011100
# 12
