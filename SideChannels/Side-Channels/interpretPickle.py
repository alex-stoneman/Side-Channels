import pickle
import myRSA


def attack():
    timings = pickle.load(open("timings.pickle", "rb"))
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
        if longer > shorter + expectedTimeDifference:
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

attack()