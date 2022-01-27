import sys, requests, bs4
import time

toFind = "https://en.wikipedia.org/wiki/Dream_SMP"
first = "https://en.wikipedia.org/wiki/Quantum_mechanics"


def find_links(link):
    linkStrings = []
    res1 = requests.get(link)
    soup1 = bs4.BeautifulSoup(res1.text, features="html.parser")
    links = soup1.select("a")
    for L in links:
        string = L.get("href")
        try:
            if string[:24] == "https://en.wikipedia.org":
                linkStrings.append([string,[]])
            #else:
             #   print(string[:24])
        except TypeError:
            pass
        if len(linkStrings) == 20:
            break
    return linkStrings


def search(myList):
    for item in myList:
        if len(item[1]) != 0:
            item[1]= search(item[1])
        else:
            item[1] = find_links(item[0])
    return  myList


linkList = [[first, []]]
for x in range(2):
    first = time.perf_counter_ns()
    linkList = search(linkList)
    for item in linkList[0][1]:
        print(item)
    second = time.perf_counter_ns()
    diff = (second - first) / (10 ** 6)
    print(f"{diff}ms")
    length = len(linkList[0][1])
    print(f"Expected time = {diff * length / 1000}s")