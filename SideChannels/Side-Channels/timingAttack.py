import subprocess, time, random
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


# test out a password 3 times and take the average in order to ensure the result is reliable
# check if this average is greater than or equal to a set value to see if this test is accepted
def mean(test, correct):
    total = 0
    for x in range(3):
        first = time.perf_counter_ns()
        interact(test)
        second = time.perf_counter_ns()
        diff = (second - first) / (10 ** 9)
        total += diff
    total /= 3
    if correct - 0.005 <= total:
        return True
    else:
        return False


# Using a timing attack to find the length of the password
def password_length_timing():
    length = 1
    interact("E")
    times = []
    # Test password lengths until one takes a significantly longer amount of time
    while True:
        length += 1
        test = "a" * length
        first = time.perf_counter_ns()
        interact(test)
        second = time.perf_counter_ns()
        diff = (second - first) / (10 ** 9)
        if length > 3:
            if diff > 4 * sum(times) / len(times):
                break
        else:
            # keep track of the average time for a response so that a particularly long one can be identified
            times.append(diff)
    return length, [diff]


# The main function for the password timing attack
# Index is used to keep track of which character in chars is being tested
# Corrections keeps track of how many times the code had to go back and fix and incorrect guess
# I made it so that if 5 corrections were made it would start again because I found if there were this
# many errors that restarting helped in removing the inconsistency
# test is the current guess for the entire password
def password_timing():
    length, times = password_length_timing()
    test = " " * length
    index = 0
    corrections = 0
    # Test up until the last character so we can see if the final one gives the correct password
    while index < length - 1:
        current = 0
        loops = 0
        while True:
            # Test for all possible characters if they increase the time for a response significantly
            first = time.perf_counter_ns()
            interact(test)
            second = time.perf_counter_ns()
            diff = (second - first) / (10 ** 9)
            correct = 0.0105 * (index + 1) + 0.004
            if correct < diff:
                if mean(test, correct):
                    break
            current += 1
            # If there has been 2 loops thorough the character set without the expected time increase
            # being found then it is likely that the previous character was incorrect
            if current > 52:
                current = 0
                loops += 1
                if corrections > 5:
                    password_timing()
                    break
                elif loops == 2:
                    # when going back into the loop the index will be 1 less to correct the previous character
                    index -= 2
                    corrections += 1
                    break
            # Change the current character in test to the newly found correct one
            test = test[:index] + chars[current] + test[index + 1:]
        index += 1
        times.append(diff)
        print(test)

    # Test the final character
    win = False
    for char in chars:
        test = test[:-1] + char
        if interact(test) == "SUCCESS!":
            print(test)
            print("Correct")
            win = True
    print(times)
    newTimes = []
    prev = times[0]
    for item in times[1:]:
        newTimes.append(round(item - prev, 4))
        prev = item
    print(newTimes)
    if not win:
        password_timing()


def time_test(test, N, d):
    first = time.perf_counter_ns()
    # interact(str(test))
    myRSA.find_time(test, d, N)
    second = time.perf_counter_ns()
    diff = (second - first) / (10 ** 9)
    return round(diff, 5)


def rsa_timing_real():
    N = 0x778db34bc38db694dfcaca7e60cb124711b5bc4db5f64808a544f82bc8b36c07
    interact("1")
    d = 1
    lesser = 0
    greater = 0
    x = 0
    Y = 0
    Z = 0
    try:
        for x in range(10):
            lesser = int(N ** (1 / (d * 2 + 1)))
            greater = int(N ** (1 / (d * 2)))
            YAverage = 0
            ZAverage = 0
            for x in range(100):
                Y = random.randint(1, lesser - 1)
                try:
                    Z = random.randint(lesser + 1, greater - 1)
                except ValueError:
                    Z = (lesser + greater) / 2
                count = 1
                for value in [Y, Z]:
                    first = time.perf_counter_ns()
                    interact(str(value))
                    second = time.perf_counter_ns()
                    diff = (second - first) / (10 ** 6)
                    if count == 1:
                        YAverage += diff
                        count += 1
                    else:
                        ZAverage += diff
            #print(YAverage)
            #print(ZAverage)
            if abs(YAverage / ZAverage) < 10:
                d *= 2
            else:
                d = d * 2 + 1
            print(d)
            print(bin(d))

    except ValueError:
        print(f"Values = {lesser, greater}")
        print(f"Y, Z = {Y, Z}")

    print(f"Finished {x}")


def rsa_timing_false():
    private = 1
    N, d = myRSA.get_external_values()
    noTests = 200
    while True:
        times = [0, 0]
        # N = 0x778db34bc38db694dfcaca7e60cb124711b5bc4db5f64808a544f82bc8b36c07
        for wanted in range(2):
            for x in range(noTests):
                while True:
                    number = random.randint(1, 100000000)
                    if square_and_multiply(number, private, N) % 2 == wanted:
                        #enter = str(hex(number))[2:]
                        enter = number
                        testTime = time_test(enter, N, d)
                        if testTime < 0.6:
                            times[wanted] += testTime
                            break
        even = times[0] / noTests
        odd = times[1] / noTests

        private *= 2
        print(even, odd)
        if even > odd + 0.028:
            private += 1
        elif even > odd + 0.02 or odd > even + 0.018:
            private //= 2
        print(bin(private))
        if private == d:
            break


def rsa_timing_grouped():
    private = 1
    # N, d = myRSA.get_external_values()
    N = 0x81cb
    d = 0x34d9
    noTests = 50
    while True:
        binaryPrivate = str(bin(private))[2:]
        times = {}
        for wanted in range(len(binaryPrivate) - 4, len(binaryPrivate)):
            if wanted >= 0:
                times[wanted] = [[], []]
                for parity in range(2):
                    repetitions = 0
                    while len(times[wanted][parity]) < noTests and repetitions < 10000:
                        count = 0
                        number = random.randint(1000, 10000000)
                        for index in range(len(binaryPrivate) - 1):
                            value = int(binaryPrivate[:index + 1])
                            evenOrOdd = square_and_multiply(number, value, N)
                            # print(number, evenOrOdd)
                            if evenOrOdd % 2 == 0:
                                count += 1
                        if count == wanted:
                            testTime = time_test(number, N, d)
                            if square_and_multiply(number, private, N) % 2 == parity:
                                times[count][parity].append(testTime)
                        else:
                            repetitions += 1
                    print(repetitions)
        print(times)
        diff = []
        collectedDiff = []
        for lists in times:
            collectedDiff.append(0)
            for x in range(len(times[lists])):
                item = times[lists][x]
                print(item)
                collectedDiff[-1] += sum(item)
                new = round(sum(item) / len(item), 4)
                times[lists][x] = new
            collectedDiff[-1] /= (2 * noTests)
            diff.append(times[lists][0] - times[lists][1])
            if diff[-1] < 0:
                diff[-1] = 0
        print(bin(d))
        print(times)
        print(f"diff = {diff}")
        print(f"Collected diff = {collectedDiff}")
        total = 0
        changed = False
        for item in diff:
            if item > 0.05:
                private = private * 2 + 1
                changed = True
                break
            total += item
        if total / len(diff) > 0.03 and not changed:
            private = private * 2 + 1
            changed = True
        if not changed:
            private = private * 2
        print(bin(private))




def rsa_timing_test():
    tests = 5
    timingTracker = {
        "Very Small": [],
        "Small": [],
        "Medium": [],
        "Large": [],
        "Very Large": []
    }
    interact("10")
    for prime in [2, 5, 7, 17]:
        for x in range(2,10):
            total = 0
            number = prime * 2 ** x
            enter = str(hex(number))[2:]
            print(enter, end=": ")
            for average in range(tests):
                difference = time_test(enter)
                total += difference
            average = round(total / tests, 5)
            print(average)
            if average <= 1:
                timingTracker["Very Small"].append(x)
            elif 1 < average <= 1.2:
                timingTracker["Small"].append(x)
            elif 1.2 < average <= 1.265:
                timingTracker["Medium"].append(x)
            elif 1.265 < average <= 1.3:
                timingTracker["Large"].append(x)
            else:
                timingTracker["Very Large"].append(x)
    for item in timingTracker:
        print(item, ":", timingTracker[item])


# rsa_timing_false()

'''
Very Small : [99]
Small : [2, 3, 11, 29, 30, 33, 37, 43, 44, 45, 49, 52, 53, 55, 59, 60, 61, 67, 71, 73, 78, 79, 85, 91]
Medium : [4, 7, 9, 13, 14, 15, 20, 26, 27, 32, 35, 40, 41, 48, 51, 57, 58, 65, 66, 81, 95, 97]
Large : [6, 17, 21, 25, 34, 46, 69, 87, 88, 93, 94]
Very Large : [5, 8, 10, 12, 16, 18, 19, 22, 23, 24, 28, 31, 36, 38, 39, 42, 47, 50, 54, 56, 62, 63, 64, 68, 70, 72, 74, 75, 76, 77, 80, 82, 83, 84, 86, 89, 90, 92, 96, 98]
'''

def many_tests():
    N, d = myRSA.get_external_values()
    largest = 0
    smallest = 10
    average = 0
    for x in range(10000):
        test = random.randint(1, 1000000)
        time = round(time_test(test, N, d), 3)
        if time > largest:
            largest = time
        if time < smallest:
            smallest = time
        average += time
        print(average / (x + 1))
    print(smallest)
    print(largest)

# many_tests()
# rsa_timing_false()
rsa_timing_grouped()