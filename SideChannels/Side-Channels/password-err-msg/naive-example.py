import subprocess,  platform
exe = './oracle.' + platform.system().lower()
p = subprocess.Popen(exe, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def interact(password):
    p.stdin.write(password.encode() + b'\n')
    p.stdin.flush()
    return p.stdout.readline().decode().strip()

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '


def write_in_base_53(num, num_digits):
    digits = []
    for _ in range(num_digits):
        digits.append(num % 53)
        num = num // 53
    return digits


length = 0
while True:
    for c in range(len(letters)**length):
        if c % 100000 == 0:
            print('checking length', length, 'checked', c, 'out of', len(letters)**length)
        digits = write_in_base_53(c, length)
        test = ''
        for d in digits:
            test += letters[d]
        x = interact(test)
        if 'SUCCESS' in x:
            print(test)
            exit()
    length += 1
