import subprocess, platform
p = subprocess.Popen('./oracle.windows', stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def interact(password):
    p.stdin.write(password.encode() + b'\n')
    p.stdin.flush()
    return p.stdout.readline().decode().strip()


def find_password_length():
    length = 1
    test = "0"
    while True:
        test2 = test * length
        if interact(test2) != "FAILURE: your pin is the wrong length":
            break
        else:
            length += 1
    return length


def find_pin(length):
    test = "0" * length
    while interact(test)[0] == "F":
        wrong = int(interact(test)[22])
        test = test[:wrong] + str(int(test[wrong]) + 1) + test[wrong + 1:]
    return test


def find_password(length):
    test = "a" * length
    while interact(test)[0] == "F":
        wrong = int(interact(test)[22])
        current = 32
        while wrong == int(interact(test)[22]):
            test = test[:wrong] + chr(current) + test[wrong + 1:]
            if current == 32:
                current = ord("a")
            elif current == ord("Z"):
                current = ord("A")
            else:
                current += 1
    return test



pswLength = find_password_length()
psw = find_password(pswLength)
print(psw)