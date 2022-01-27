import subprocess, platform, time
exe = './oracle.' + platform.system().lower()
p = subprocess.Popen(exe, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def interact(password):
    p.stdin.write(password.encode() + b'\n')
    start = time.time()
    p.stdin.flush()
    result = p.stdout.readline().decode().strip()
    delay = time.time() - start
    return result, delay

# here's some code that tests if 'PaSSword' is the password
# delete it and replace it with your own code that works out the correct password
test = 'PaSSword'
result, delay = interact(test)
if 'SUCCESS' in result:
    print('the password is', test)
else:
    print('the password is not', test)
    print("The delay was", delay)

# The delay might vary due a variety of factors, how might we get a more reliable value?