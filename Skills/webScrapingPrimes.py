import sys, requests, bs4


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


res1 = requests.get("https://mersenne.org/primes/")
text = res1.text
first = True
for x in range(len(text)):
    segment = text[x: x + 15]
    if segment == "report_exponent" and first == False:
        prime_start = x + 24
        prime_finish = x + 24
        while text[prime_finish] != '"':
            prime_finish += 1
        exponent = find_number(text[prime_start:prime_finish])
        if exponent != "no":
            print(exponent)
            print(f"(2^{exponent}) -1 = {2 ** exponent - 1}")
    else:
        first = False
print("finished")