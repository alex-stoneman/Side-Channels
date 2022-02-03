import subprocess, time, math, random

# At the moment the challenge is set manually because I wasn't sure if I wanted to make
# p global or If I wanted to pass it thorough as a parameter like in errorMsg
chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
problem = "password-timing"
exe = f"./{problem}/oracle.windows"
p = subprocess.Popen(exe, stdin=subprocess.PIPE, stdout=subprocess.PIPE)


# test out a password and return the error message, ignore OS errors bc they were annoying
def interact(password):
    try:
        p.stdin.write(password.encode() + b'\n')
        p.stdin.flush()
        return p.stdout.readline().decode().strip()
    except OSError:
        pass


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


def rsa_timing():
    N = 0x778db34bc38db694dfcaca7e60cb124711b5bc4db5f64808a544f82bc8b36c07
    interact("1")
    d = 1
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
        print(f"X, Y = {Y, Z}")


    print(f"Finished {x}")
rsa_timing()





