import subprocess
chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
problem = ["pin-four-digit", "pin-err-msg", "password-err-msg"]


# Find the integer index in the error message and return it
def find_number(text):
    final = ""
    integers = "1234567890"
    for character in text:
        if character in integers:
            final += character
    if final != "":
        return int(final)
    else:
        return "no"


# test out a password and return the error message, ignore OS errors bc they were annoying
def interact(password, p):
    try:
        p.stdin.write(password.encode() + b'\n')
        p.stdin.flush()
        return p.stdout.readline().decode().strip()
    except OSError:
        pass


# Keep incrementing the password length by 1 until it is correct then return this length
def find_password_length(p):
    length = 1
    test = "0"
    while True:
        test2 = test * length
        if interact(test2, p)[-16:] != "the wrong length":
            break
        else:
            length += 1
    return length


# For a pin of a known length change each number in the pin in turn until it is correct
# Use the value from the find_number() function to see which number in the pin needs to be changed
def find_pin(length, p):
    test = "0" * length
    while interact(test, p)[0] == "F":
        wrong = find_number(interact(test, p))
        test = test[:wrong] + str(int(test[wrong]) + 1) + test[wrong + 1:]
    return test


# For password of a known length change each character in the password in turn ... you get the idea
# Same as the pin but with letters
def find_password(length, p):
    test = "a" * length
    error = "F"
    while error == "F":
        wrong = find_number(interact(test, p))
        current = 0
        while wrong == find_number(interact(test, p)):
            test = test[:wrong] + chars[current] + test[wrong + 1:]
            current += 1
            error = interact(test, p)[0]

    return test


# When this function is called from the main file it is passed which challenge it is doing
# Open the appropriate file and then the appropriate functions
def run(option):
    exe = f"./{problem[int(option) - 1]}/oracle.windows"
    p = subprocess.Popen(exe, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    if option == "1":
        print(find_pin(4, p))
    else:
        length = find_password_length(p)
        if option == "2":
            print(find_pin(length, p))
        else:
            print(find_password(length, p))
