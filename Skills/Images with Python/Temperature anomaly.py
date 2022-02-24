from PIL import Image
from math import floor
import csv

#climate.show()
values = []

with open("global land and ocean anomaly.csv") as csvfile:
    fileReader = csv.reader(csvfile, delimiter = ",")
    for row in fileReader:
        if row[1] != "Land & Ocean":
            values.append(float(row[1]))

def main_curve(num):
    return -(num ** 2) + 1

def lesser_curve(num):
    return -3 * (num ** 2) + 1


climate = Image.new("RGB", (5 * len(values), 500))
count = 0
for line in values:
    if line > 0:
        red = floor(255 * main_curve(line))
        others = floor(255 * lesser_curve(line))
        colour = (red, others, others)
    elif line < 0:
        blue = floor(255 * main_curve((abs(line))))
        others = floor(255 * lesser_curve(abs(line)))
        colour = (others, others, blue)
    else:
        colour = (255, 255, 255)
    for x in range(5):
        for y in range(500):
            climate.putpixel((count, y), colour)
        count += 1

climate.show()
