import random
from PIL import Image
import math

penguin = Image.open("Penguins.jpg")
maxHeight = penguin.height
maxWidth = penguin.width

def vernam_image():
    data = ""
    vernam = ""
    for item in penguin.getdata():
        for value in item:
            data += str(bin(value))[3:]

    print(data, "\n")
    for x in range(len(data)):
        vernam += random.choice(["0", "1"])
    print(vernam)
    scambled = Image.new("RGB", (maxWidth, maxHeight))

    for y in range(maxHeight):
        for x in range(maxWidth):
            start = y * maxWidth + 24 * x - 1
            first = 0

def grey_scale():
    for row in range(maxWidth):
        for column in range(maxHeight):
            values = penguin.getpixel((row, column))
            average = 0
            for item in values:
                average += item
            average //= 3
            penguin.putpixel((row, column), (average, average, average))
    penguin.show()