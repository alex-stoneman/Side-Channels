# the pin is 4 digits
pin = "????"

def check():
    attempt = input()

    if len(attempt) != 4:
        print("FAILURE: your pin is not 4 digits")
        return

    i = 0
    while i < len(pin):
        if pin[i] != attempt[i]:
            print(f"FAILURE: the digit at", i, "is wrong")
            return
        i = i + 1

    print("SUCCESS!")
    exit()

while True:
    check()
