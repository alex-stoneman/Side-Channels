from matplotlib import pyplot as plt

timings = []
file = open("logResults.txt", "r")
for line in file:
    #print(line)
    timings.append([])
    for item in line.split(","):
        try:
            timings[-1].append(float(item))
        except ValueError:
            pass

file.close()
count = 0
for time in timings:
    count += 1
    print("e")
    plt.plot(time, [count for x in range(len(time))])
plt.show()