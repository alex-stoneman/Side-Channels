import GenaratePokeBase
from squirdle import get_sql_query

def search():
    limits = {
        "names": [],
        "height": [float(input("min height ")), float(input("Max height "))],
        "weight": [float(input("min weight ")), float(input("Max weight "))],
        "gen": [int(input("min gen ")), int(input("max gen "))],
        "first_type": [[], input("Input if type 1 known: ")],
        "last_type": [[], input("Input if type 2 known: ")]
    }
    if len(limits["first_type"][1]) == 0:
        pokeType = ""
        while pokeType != "stop":
            pokeType = input("Input incorrect type:")
            limits["first_type"][0].append(pokeType)
            limits["last_type"][0].append(pokeType)
    query = get_sql_query(limits)
    for item in GenaratePokeBase.external_query(query):
        print(item)


while True:
    choice = input("A: Search, B: Pokemon data, X: Exit\n")
    if choice.upper() == "A":
        search()
    elif choice.upper() == "B":
        print(GenaratePokeBase.external_query(f"SELECT * FROM pokebase WHERE pokemon = \"{input('pokemon name: ')}\";"))
    elif choice.upper() == "X":
        break