# the pin is some number of digits
pin = "???..."

def check():
    attempt = input()

    if len(pin) != len(attempt):
        print("FAILURE: your pin is the wrong length")
        return

    i = 0
    while i < len(pin):
        if pin[i] != attempt[i]:
            print("FAILURE: the character at", i, "is wrong")
            return
        i = i + 1

    print("SUCCESS!")
    exit()

while True:
    check()
