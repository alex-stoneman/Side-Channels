import subprocess, platform
exe = './oracle.' + platform.system().lower()
p = subprocess.Popen(exe, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def interact(password):
    p.stdin.write(password.encode() + b'\n')
    p.stdin.flush()
    return p.stdout.readline().decode().strip()

# here's some code that tests if 'PaSSword' is the password
# delete it and replace it with your own code that works out the correct password
test = 'PaSSword'
result = interact(test)
if 'SUCCESS' in result:
    print('the password is', test)
else:
    print('the password is not', test)
