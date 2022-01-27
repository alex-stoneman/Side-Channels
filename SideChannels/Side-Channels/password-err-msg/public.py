# the password is some number of upper and lower case letters plus spaces
password = "???..."

def check():
    attempt = input()

    if len(password) != len(attempt):
        print("FAILURE: your password is the wrong length")
        return

    i = 0
    while i < len(password):
        if password[i] != attempt[i]:
            print("FAILURE: the character at", i, "is wrong")
            return
        i = i + 1

    print("SUCCESS!")

while True:
    check()
#(where applicable)