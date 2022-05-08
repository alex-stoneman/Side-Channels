import subprocess
chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
problem = ["pin-four-digit", "pin-err-msg", "password-err-msg"]

# test out a password and return the error message
def interact(password, p):
    p.stdin.write(password.encode() + b'\n')
    p.stdin.flush()
    return p.stdout.readline().decode().strip()


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
        wrongIndex = find_number(interact(test, p))
        test = test[:wrongIndex] + str(int(test[wrongIndex]) + 1) + test[wrongIndex + 1:]
    return test


# For password of a known length change each character in the password in turn ... you get the idea
# Same as the pin but with letters instead of digits
def find_password(length, p):
    test = "a" * length
    error = "F"
    while error == "F":
        wrongIndex = find_number(interact(test, p))
        current = 0
        while wrongIndex == find_number(interact(test, p)):
            test = test[:wrongIndex] + chars[current] + test[wrongIndex + 1:]
            current += 1
            error = interact(test, p)[0]

    return test


# When this function is called it is passed which challenge it is doing
# Open the appropriate file and then run the appropriate functions
def run(option):
    exe = f"./{problem[int(option) - 1]}/oracle.windows"
    p = subprocess.Popen(exe, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    if option == "1":
        # The length is already know so this doesn't need to be found
        print(find_pin(4, p))
    else:
        # both problems require the length to be found first
        length = find_password_length(p)
        if option == "2":
            print(find_pin(length, p))
        else:
            print(find_password(length, p))

run(input(": "))