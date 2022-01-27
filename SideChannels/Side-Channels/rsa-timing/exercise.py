import time, subprocess, platform, random
exe = './oracle.' + platform.system().lower()

N = 0xce147b31d8f218c76723f430f18ae1a9
e = 0x10001
d = 0x2819341f6ee72c8ac6bcbdc258089341

cmd = [exe]
# To attack the real secret value comment out the next line
cmd += ['-mod', '{:x}'.format(N), '-priv', '{:x}'.format(d)]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def interact(x):
    p.stdin.write('{:x}'.format(x).encode() + b'\n')
    start = time.time()
    p.stdin.flush()
    result = p.stdout.readline()
    delay = time.time() - start
    return delay


ciphertexts = [random.randrange(2, N) for _ in range(100)]
timings = [interact(c) for c in ciphertexts]

# I've pre-recorded some timings for you if you want to save some time
# import pickle
# with open('timings.pickle', 'rb') as f:
#     ciphertexts, timings = pickle.load(f)


def check(d_guess):
    return False


d_guess = 0x12345
print(d_guess)
if check(d_guess):
    print('found d =', hex(d_guess))
else:
    print('failed')