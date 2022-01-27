from time import sleep
password = "???..."


def check():
    attempt = input()

    if len(password) != len(attempt):
        print("FAILURE")
        return

    i = 0
    while i < len(password):
        sleep(0.1)
        if password[i] != attempt[i]:
            print("FAILURE")
            return
        i = i + 1

    print("SUCCESS!")

while True:
    check()
    
