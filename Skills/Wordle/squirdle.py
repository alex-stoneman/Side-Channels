import time

import mysqlx

import GenaratePokeBase
import selenium
from numpy import unicode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# outputs = {129001: "correct", 128997: "incorrect", 129000: "different", 128316: "more", 128317: "less"}
outputs = {"R": "correct", "W": "incorrect", "V": "incorrect", "2": "different", "x": "more", "y": "less"}


class pokemon:
    def __init__(self, n, f, l, h, w, g):
        self.name = n
        self.first_type = f
        self.last_type = l
        self.height = h
        self.weight = w
        self.gen = g
        self.score = 0

    def find_score(self, limits):
        self.score = 0
        if len(limits["gen"]) != 1:
            self.score += (((float(limits["gen"][0]) + float(limits["gen"][1])) / 2) - float(self.height)) ** 2 * 3
        if len(limits["height"]) != 1:
            self.score += (((float(limits["height"][0]) + float(limits["height"][1])) / 2) - float(self.height)) ** 2
        if len(limits["weight"]) != 1:
            self.score += (((float(limits["weight"][0]) + float(limits["weight"][1])) / 2) - float(self.weight)) ** 2


# Using Chrome to access web
# Open the website
def enter_guess(pokemon_name, driver):
    driver.find_element_by_id('guess').send_keys(pokemon_name)
    #driver.find_elements_by_css_selector("Body").send_keys(Keys.RETURN)
    try:
        driver.find_elements_by_css_selector("Form")[0].find_elements_by_css_selector("input")[2].send_keys(Keys.RETURN)
    except selenium.common.exceptions.ElementNotInteractableException:
        print("Test 1")
        elem = driver.find_element_by_id("guess")
        print("Test 2")
        ac = selenium.webdriver.common.action_chains.ActionChains(driver)
        print("Test 3")
        ac.move_to_element(elem).move_by_offset(-300, -20).click()
        print("Test 4")
        driver.find_elements_by_css_selector("Form")[0].find_elements_by_css_selector("input")[2].send_keys(Keys.RETURN)
    driver.get('https://squirdle.fireblend.com/')
    values = []
    #read the results...
    #iterate over column
    #for col in columns[:-1]:
    #    s = col.find_elements_by_css_selector("p")[0].text
    #    values.append(ord(s))
    #return values
    while True:
        try:
            columns = driver.find_elements_by_css_selector(".row")[-1].find_elements_by_css_selector(".column")
            for col in columns[:-1]:
                s = col.screenshot_as_base64[64]
                values.append(outputs[s])
                print(s, end = ", ")
            print()
            break
        except KeyError:
           print("Error 001")
    return values

def new_game(driver):
    driver.find_elements_by_css_selector("Form")[0].find_elements_by_css_selector("Button")[0].send_keys(Keys.RETURN)


def check_number(attribute, value, guess, limits):
    if value == "correct":
        limits[attribute] = [getattr(guess, attribute)]
    elif value == "more":
        limits[attribute][0] = getattr(guess, attribute)
    elif value == "less":
        limits[attribute][1] = getattr(guess, attribute)
    else:
        print("BAD THINGS")


def check_type(attribute, value, guess, limits):
    if value == "correct":
        limits[attribute][1] = getattr(guess, attribute)
    elif value == "incorrect":
        limits["first_type"][0].append(getattr(guess, attribute))
        limits["last_type"][0].append(getattr(guess, attribute))
    elif value == "different":
        if attribute == "first_type":
            limits["last_type"][1] = guess.first_type
        else:
            limits["first_type"][1] = guess.last_type
    else:
        print("BAD THINGS")


def get_sql_query(limits):
    query = "SELECT * FROM pokebase WHERE"
    # Not a previous pokemon
    for pokeName in limits["names"]:
        query += f" pokemon != \"{pokeName}\" and"
    # height margins
    if len(limits["height"]) == 1:
        query += f" height = {limits['height'][0]} and"
    else:
        query += f" height > {limits['height'][0]} and height < {limits['height'][1]} and"
    # weight margins
    if len(limits["weight"]) == 1:
        query += f" weight = {limits['weight'][0]} and"
    else:
        query += f" weight > {limits['weight'][0]} and weight < {limits['weight'][1]} and"
    # generation margins
    if len(limits["gen"]) == 1:
        query += f" generation = {limits['gen'][0]}"
    else:
        query += f" generation > {limits['gen'][0]} and generation < {limits['gen'][1]}"
    # first typing
    if len(limits["first_type"][1]) != 0:
        query += f" and first_type = '{limits['first_type'][1]}'"
    else:
        for pokeType in limits["first_type"][0]:
            query += f" and first_type != '{pokeType}'"
    # second typing
    if len(limits["last_type"][1]) != 0:
        query += f" and last_type = '{limits['last_type'][1]}'"
    else:
        for pokeType in limits["last_type"][0]:
            query += f" and last_type != '{pokeType}'"
    query += ";"
    return query


def main():
    driver = webdriver.Chrome('./chromedriver')
    driver.get('https://squirdle.fireblend.com/')
    try:
        while True:
            guess = pokemon("Bibarel", "normal", "water", 1, 31.5, 4)
            limits = {
                "height": [0.0, 20.1],
                "weight": [0.0, 1000.0],
                "gen": [0, 9],
                "first_type": [[], ""],
                "last_type": [[], ""],
                "names":[]}
            while True:
                limits["names"].append(guess.name)
                feedback = enter_guess(guess.name, driver)
                print(feedback)
                check_number("gen", feedback[0], guess, limits)
                check_type("first_type", feedback[1], guess, limits)
                check_type("last_type", feedback[2], guess, limits)
                check_number("height", feedback[3], guess, limits)
                check_number("weight", feedback[4], guess, limits)
                query = get_sql_query(limits)
                possiblePokemon = GenaratePokeBase.external_query(query)
                print(possiblePokemon)
                words = driver.find_elements_by_css_selector('body')[0].text
                if "You won!" in words:
                    new_game(driver)
                    print("success")
                    break
                elif "You lost! The secret Pokémon was" in words:
                    print("Pokemon missing or incorrect data")
                    msg = "You lost! The secret Pokémon was"
                    start = words.index(msg) + len(msg)
                    print(words[start: start + 20])
                    print(guess.name)
                    new_game(driver)
                    break
                else:
                    pass
                if len(possiblePokemon) == 0:
                    print(guess.name)
                    print("problem with data")
                    break
                pokemonObjects = []
                guess.score = 0
                for item in possiblePokemon:
                    pokemonObjects.append(pokemon(item[0], item[1], item[2], item[3], item[4], item[5]))
                    pokemonObjects[-1].find_score(limits)
                    if pokemonObjects[-1].score >= guess.score:
                        guess = pokemonObjects[-1]
    except selenium.common.exceptions:
        print("bad")
        input("Close:")
        driver.close()

    except:
        driver.close()
        print("Very bad")


if __name__ == "__main__":
    main()
    #driver = webdriver.Chrome('./chromedriver')
    #driver.get('https://squirdle.fireblend.com/')
    #guess = pokemon("Bibarel", "normal", "water", 1, 31.5, 4)
    #enter_guess(guess.name)
    #x = input()
    #driver.close()

# Castform
# Mew
# Mr.Rime - Maybe fixed, can't remember
# Kabootops
