import mysql.connector
import pandas as pd
psw = [108,81,115,121,40,55,80,56,87,41]
pw = ""
for item in psw:
  pw += chr(item)
#
#
# Go to services and manually start MySQL80 to use
#
#
def create_server_connection(host_name, user_name, user_password, db_name):
  connection = None
  try:
    connection = mysql.connector.connect(
      host=host_name,
      user=user_name,
      passwd=user_password,
      database=db_name
    )
    #print("MySQL Database connection successful")
  except mysql.connector.Error as err:
    print(f"Error: '{err}'")

  return connection


def create_database(connection, query):
  cursor = connection.cursor()
  try:
    cursor.execute(query)
    print("Database created successfully")
  except mysql.connector.Error as err:
    print(f"Error: '{err}'")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
      cursor.execute(query)
      connection.commit()
      print("Query successful")
    except mysql.connector.Error as err:
      print(f"Error: '{err}'")



connection = create_server_connection("localhost", "root", pw, "pokebase")
#print(connection)

# create_database_query = "CREATE DATABASE pokebase"
# create_database(connection, create_database_query)

create_pokebase_table = """
CREATE TABLE pokebase (
  pokemon VARCHAR(40) PRIMARY KEY,
  first_type VARCHAR(20) NOT NULL,
  last_type VARCHAR(20) NOT NULL,
  height DECIMAL(4,1) NOT NULL,
  weight DECIMAL(4,1) NOT NULL,
  generation TINYINT NOT NULL
  );
 """

# execute_query(connection, create_pokebase_table)

def read_query(connection, query):
  cursor = connection.cursor()
  result = None
  try:
    cursor.execute(query)
    result = cursor.fetchall()
    return result
  except mysql.connector.Error as err:
    print(f"Error: '{err}'")


def possible_pokemon(connection, test_query):
  pokemonList = []
  results = read_query(connection, test_query)
  try:
    for result in results:
      pokemonList.append(result)
  except TypeError:
    pass
  return pokemonList


def external_query(query):
  connection = create_server_connection("localhost", "root", pw, "pokebase")
  pokemonList = possible_pokemon(connection, query)
  return pokemonList

#test = "SELECT pokemon, weight FROM pokebase WHERE weight >= 900;"
#possible_pokemon(test)
#test = "SELECT * FROM pokebase WHERE pokemon = 'wishiwashi school form';"
#print(read_query(connection, test))