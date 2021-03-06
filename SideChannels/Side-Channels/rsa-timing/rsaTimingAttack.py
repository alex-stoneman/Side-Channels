import subprocess, time, random, pickle
import myRSA
from matplotlib import pyplot as plt

exe = f"./oracle.windows"
p = subprocess.Popen(exe, stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def wipe_file(filename):
    file = open(filename, "w")
    file.write("0.01,1\n")
    file.close()


def record_result(result, position, filename):
    file = open(filename, "a")
    file.write(f"{result},{position}\n")
    file.close()


def plot_results(length, filename, practise):
    results = [[], []]
    positions = [[], []]
    finalDecision = []
    listOfTimes = []
    file = open(filename, "r")
    for line in file:
        listOfTimes.append(line.split(","))
    file.close()
    if practise:
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

    else:
        for items in listOfTimes:
            if float(items[0]) < 0.001:
                results[0].append(float(items[0]))
                positions[0].append(int(items[1]))
            else:
                results[1].append(float(items[0]))
                positions[1].append(int(items[1]))
        plt.plot(results[1], positions[1], "ob", label="1")
        plt.plot(results[0], positions[0], "or", label="0")
        plt.vlines(0.001, 0, length, "g")
    plt.legend()
    plt.xlabel("Average time Difference")
    plt.ylabel("Bit number")
    yInt = []
    difference = length // 12
    value = 1
    while value < length:
        yInt.append(value)
        value += difference
    yInt.append(value)
    plt.yticks(yInt)
    plt.show()


def which_key():
    file = open("test-numbers.txt", "r")
    count = 1
    values = []
    for line in file:
        whereInFile = (count - 3) % 6
        if whereInFile in [0, 1, 2]:
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


# Successful for 32 bit primes using 80 tests - took ~ 70 minutes
# Inefficient use of tests
# Using the practise keys with a delay of 0.01s
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
        # Two next two possibilities to see if either work as a solution
        if myRSA.actual_square_and_multiply(encrypted, 2 * private + 1, N) == 65:
            private = private * 2 + 1
            record_result(0.01, len(str(bin(private))) - 2, "recordedTiming.txt")
            break
        elif myRSA.actual_square_and_multiply(encrypted, 2 * private, N) == 65:
            private = private * 2
            record_result(0, len(str(bin(private))) - 2, "recordedTiming.txt")
            break
        # Generate random values, sort them into ones which will be divisible by 2 at this stage in the
        # Square and multiple calculation until there are a suitable number of tests for both categories
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
        # Find the average time
        longer = times[0][0] / noTests
        shorter = times[1][0] / noTests
        print(longer - shorter)
        if 4 * expectedTimeDifference > longer - shorter > expectedTimeDifference:
            private = private * 2 + 1
            if repeat > 1:
                repeat -= 2
            elif repeat == 1:
                repeat = 0
            record_result(round(longer - shorter, 6), len(str(bin(private))) - 2, "recordedTiming.txt")
        elif longer < shorter + 0.75 * expectedTimeDifference:
            private *= 2
            repeat += 1
            record_result(round(longer - shorter, 6), len(str(bin(private))) - 2, "recordedTiming.txt")
        else:
            reallyRepeat += 1
            if reallyRepeat > 4 or abs(longer - shorter) > 25 * expectedTimeDifference:
                private //= 2
                reallyRepeat = 0
            record_result(round(longer - shorter, 6), len(str(bin(private))) - 1, "recordedTiming.txt")
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
    plot_results(len(str(bin(d))) - 2, "recordedTiming.txt", True)


def attack_using_pickle():
    timings = pickle.load(open("../timings.pickle", "rb"))
    N = 0x778db34bc38db694dfcaca7e60cb124711b5bc4db5f64808a544f82bc8b36c07
    e = 0x10001
    private = 1
    expectedTimeDifference = 0.001
    encrypted = myRSA.actual_square_and_multiply(65, e, N)
    # even, odd - longer, shorter
    while myRSA.actual_square_and_multiply(encrypted, private, N) != 65:
        times = [[0, 0], [0, 0]]
        if myRSA.actual_square_and_multiply(encrypted, 2 * private + 1, N) == 65:
            private = private * 2 + 1
            print("Ending here?")
            print(myRSA.actual_square_and_multiply(encrypted, private, N))
            break
        elif myRSA.actual_square_and_multiply(encrypted, 2 * private, N) == 65:
            private *= 2
            print("Or here?")
            print(myRSA.actual_square_and_multiply(encrypted, private, N))
            break

        for x in range(len(timings[0])):
            value = timings[0][x]
            previous, expected = myRSA.counting_square_and_multiply(value, private, N)
            expected = (expected ** 2) % N
            parity = expected % 2
            times[parity][0] += timings[1][x]
            times[parity][1] += 1


        longer = times[0][0] / times[0][1]
        shorter = times[1][0] / times[1][1]
        difference = longer - shorter
        record_result(round(difference, 6), len(str(bin(private))) - 2, "pickleTimeDifference.txt")
        if difference > expectedTimeDifference:
            private = private * 2 + 1
        else:
            private *= 2
        for item in times:
            print(item)
        print(longer, shorter)
        print(longer - shorter)
        print(bin(private))
        print()
    print("\n" * 5)
    print(bin(private))



# wipe_file("pickleTimeDifference.txt")
# attack_using_pickle()
plot_results(256, "pickleTimeDifference.txt", False)
