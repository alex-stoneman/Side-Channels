import csv
from scipy.stats import t
import matplotlib.pyplot as plt
import math


def find_a_coefficient(y_average, b, x_average):
    return y_average - b * x_average


def find_b_coefficient(n, xSum, ySum, xSquaredSum, xySum):
    sxy = xySum - (xSum * ySum) / n
    variance = xSquaredSum - (xSum ** 2) / n
    return sxy / variance


def central_values(data):
    n = len(data[0])
    xSum = 0
    ySum = 0
    xSquaredSum = 0
    xySum = 0
    for item in data[0]:
        xSum += item
        xSquaredSum += item ** 2
    for item in data[1]:
        ySum += item
    xMean = xSum / n
    yMean = ySum / n
    for number in range(n):
        xySum += data[0][number] * data[1][number]
    sxx = xSquaredSum - n * xMean ** 2
    return n, xMean, yMean, xSum, ySum, xSquaredSum, xySum, sxx


def abt_difference(residuals, n, sxx, xMean, alpha):
    rSquaredSum = 0
    for number in residuals:
        rSquaredSum += number ** 2
    MSE = rSquaredSum / (n - 2)
    alpha /= 2
    atCoeff = math.sqrt(MSE * ((1 / n) * ((xMean ** 2) / sxx)))
    btCoef = math.sqrt(MSE / sxx)
    aDiff = t.ppf(alpha, n - 2) * atCoeff
    bDiff = t.ppf(alpha, n - 2) * btCoef
    return aDiff, bDiff



failed = False
try:
    data = []
    with open("errorData.csv") as csvfile:
        fileReader = csv.reader(csvfile, delimiter=",")
        for row in fileReader:
            data.append([])
            for item in row:
                data[-1].append(int(item))
    if len(data[0]) != len(data[1]):
        raise IndexError
except ValueError:
    print("Error in data")
    failed = True
except IndexError:
    print("There needs to be the same number of x and y values")
    failed = True

if not failed:
    displayData = [data[0], []]
    n, xMean, yMean, xSum, ySum, xSquaredSum, xySum, sxx = central_values(data)
    b = find_b_coefficient(n, xSum, ySum, xSquaredSum, xySum)
    a = find_a_coefficient(yMean, b, xMean)
    print(f"y = {round(b, 5)}x + {round(a, 5)}")
    print("Residuals:")
    residualValues = []
    for x in range(n):
        foundValue = b * data[0][x] + a
        displayData[1].append(foundValue)
        error = str(round(data[1][x] - foundValue, 6))
        residualValues.append(float(error))
        print(" " * (14 - len(error)) +  error)

    plt.scatter(data[0], data[1], color= "black")
    plt.scatter(displayData[0], displayData[1], color="red")
    plt.plot(displayData[0], displayData[1])
    for x in range(n):
       plt.plot([data[0][x], data[0][x]], [data[1][x],displayData[1][x]], color="black")
    #
    plt.show()

    for x in range(1, 50):
        alpha = x / 50
        aDiff, bDiff = abt_difference(residualValues, n,sxx, xMean, alpha)
        print(aDiff, bDiff)
        highY = []
        lowY = []
        for number in data[0]:
            highY.append((b + bDiff) * number + a + aDiff)
            lowY.append((b - bDiff) * number + a - aDiff)
        plt.plot(data[0], highY, "b--")
        plt.plot(data[0], lowY, "g--")
        print(data[0])
        print(highY)
        print(lowY)
    plt.show()