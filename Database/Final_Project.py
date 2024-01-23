import mysql.connector

connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        database="zombiator",
        user="root",
        password="Bu@1234#Li",
        autocommit=True
    )
countries = []
sql1 = "SELECT country FROM airport"
cursor = connection.cursor()
cursor.execute(sql1)
result1 = cursor.fetchall()
countries = result1

#1
def get_dict_airportcoordinate_by_country(country):
    dict_airport_coordinate = {}
    sql = "SELECT country, latitude_deg, longitude_deg FROM airport"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            coordinate = (row[1], row[2])
            dict_airport_coordinate[row[0]] = coordinate
    return dict_airport_coordinate

#2

import get_dict_airportcoordinate_by_country
from geopy.distance import geodesic
def calculate_distance(current_location, destination):
    now_location = get_dict_airportcoordinate_by_country(current_location).get(current_location)
    now_destination = get_dict_airportcoordinate_by_country(destination).get(destination)
    distance = geodesic(now_location,now_destination).km
    return distance

#3
def get_dict_distance(current_location):
    dict_distance = {}
    dict_airport_coordinate = get_dict_airportcoordinate_by_country(countries)
    for country in dict_airport_coordinate:
        distance = calculate_distance(current_location,country)
        dict_distance[country] = distance
    return dict_distance

#4

def calculate_maxdistance(user_money,user_fuel):
    money_to_fuel = user_money / 10
    fuelmax = money_to_fuel + user_fuel
    max_distance = fuelmax * 10
    return max_distance

#5

def need_more_money(max_distance,current_location):
    dict_distance = get_dict_distance(current_location)
    list_distance = []
    for country in dict_distance:
        if dict_distance[country] != 0:
          list_distance.append(dict_distance[country])
    return max_distance < min(list_distance)

#6

def fuel_consumed(distance):
    need_fuel = distance/10
    return need_fuel


    distance = (float(input("Enter the current distance you've travelled: ")))
    need_fuel = fuel_consumed(distance)
    print(f"The fuel you used was {need_fuel:.2f} liters.")
# If it is not the number input...



#7

def convert_fuel_money(amount_fuel):
    spent_money = amount_fuel * 10
    return spent_money

    amount_fuel = (float(input("Enter the amount of fuel you want to buy in liters: ")))
    spent_money = convert_fuel_money(amount_fuel)
    print(f"The money you have to spend is {spent_money:.2f} euros.")



def convert_fuel_money(amount_fuel, fuel_price=10):
    return amount_fuel * fuel_price


while True:
        amount_fuel = (float(input("Enter the amount of fuel you want to buy in liters: ")))
        spent_money = convert_fuel_money(amount_fuel)

        current_money = (float(input("Enter your current amount of money: ")))

        if current_money >= spent_money:
            current_money -= spent_money
            print(f"The money you have to spend is {spent_money:.2f} euros.")
            print(f"The remaining amount of money is {current_money:.2f} euros.")
            break

        else:
            print("Cannot purchase. Please enter less amount of fuel.")



#8

import get_dict_distance as dis
import random
import dbconnection as db

condition_and_reward = {}
difficult = ["easy", "normal", "hard"]


def need_weapon_and_reward():
    list_country = dis.get_dict_distance("Finland")
    count = 0
    for country in list_country:
        if count == 4 and "hard" in difficult:
            difficult.remove("hard")
        difficult_level = random.choice(difficult)
        if difficult_level == "hard":
            count += 1
        sql = "SELECT name, min_amount, max_amount, difficult_level, passing_condition FROM reward"
        reward = []
        cursor = db.db_connection()
        cursor.execute(sql)
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            reward.append(difficult_level)
            for row in result:
                if row[3] == difficult_level:

                    if row[0] == "money" or row[0] == "weapon":
                        reward.append(random.randint(row[1], row[2]))
                        reward.append(row[4])
            reward.pop(2)
            condition_and_reward[country] = reward
    return condition_and_reward

#9 player

def is_player_existed(player_name):
    sql = "SELECT id, name FROM player WHERE name = %s"
    values = (player_name,)

    cursor = db.db_connection()
    cursor.execute(sql, values)
    if cursor.rowcount > 0:
        return True

    return False


def get_player_info(player_name):
    sql = "SELECT id, name FROM player WHERE name = %s"
    values = (player_name,)

    cursor = db.db_connection()
    cursor.execute(sql, values)

    player_info = cursor.fetchone()

    if player_info:
        return player_info
    else:
        return None


def add_player(name, location):
    sql = "INSERT INTO player (name, location) VALUES (%s, %s)"
    values = (name, location)

    cursor = db.db_connection()
    cursor.execute(sql, values)


def update_player(name, new_location):
    sql = "UPDATE player SET location = %s WHERE name = %s"
    values = (new_location, name)

    cursor = db.db_connection()
    cursor.execute(sql, values)

#10 ranking

def add_ranking(player_id, score):
    sql = "INSERT INTO ranking (player_id, score) VALUES (%s, %s)"
    values = (player_id, score)

    cursor = db.db_connection()
    cursor.execute(sql, values)


def update_player_score(player_id, new_score):
    sql = "UPDATE ranking SET score = %s WHERE player_id = %s"
    values = (new_score, player_id)

    cursor = db.db_connection()
    cursor.execute(sql, values)


def get_all_player_ranking():
    sql = "SELECT player.name, ranking.score FROM ranking JOIN player ON ranking.player_id = player.id ORDER BY ranking.score DESC"

    cursor = db.db_connection()
    cursor.execute(sql)

    # Fetch all rows as a list of tuples
    rankings = cursor.fetchall()

    return rankings


def get_ranking_info(player_id):
    sql = "SELECT * FROM ranking WHERE player_id = %s"
    values = (player_id,)

    cursor = db.db_connection()
    cursor.execute(sql, values)

    ranking_info = cursor.fetchone()

    if ranking_info:
        return ranking_info
    else:
        return None

#11
def list_airport(max_distance, dict_distance):
    for country in dict_distance:
        if 0 < dict_distance[country] <= max_distance:
            print(f"{country} {dict_distance[country]} km")

#main beginning

user_money = 500
user_fuel = 150
user_weapon = 200
final_weapon = 2000
final_reward = 10000
current_location = "Finland"

name = input("Please enter your name:")
print(f"Welcome to Zombiator,{name}!\nYou are going to save the world!\nNow start!")

while user_weapon < final_weapon:
    max_distance = calculate_maxdistance(user_money,user_fuel)
    dict_distance = get_dict_distance(current_location)
    if (need_more_money(max_distance,current_location) or user_weapon) <= 50:
        user_money = user_money + 50
        user_weapon = user_weapon + 150

#main_2

command = input("Choose option: \n")
if command == "2":
    # Assume maximum distance (from def calculate_maxdistance(player_money, player_fuel) function)
    max_distance = float(input("Enter the maximum distance: "))
    # Assume distance from other countries
    dict_distance = {"Country1": 120.45, "Country2": 8397.43, "Country3": 12345, "Country4": 24.5}
    player_money = 3349  # Assume the player's money remaining
    player_fuel = 70  # Assume the player's fuel remaining
    player_weapon = 534  # Assume the player's weapons remaining
    # Display player's profile
    print(f"You have:\n{player_money} euros.\n{player_fuel} liters of fuel.\n{player_weapon} weapons")
    print("\nList of airports currently accessible with your fuel and money at present:")
    list_airport(max_distance, dict_distance)


#main_3
if command == "3":
        while True:
            amount = int(input("Enter how much fuel do you want to buy: "))
            price_per_unit = 10  # Assuming the price per unit of fuel is 10 euros
            spent_money = amount * price_per_unit

            if user_money >= spent_money:
               user_money -= spent_money
               user_fuel += amount
               print(f"You have purchased {amount}l of fuel.")
               print(f"Your remaining balance is {user_money} euros.")
               break
            else:
                print("Insufficient funds. Please enter a smaller quantity or quit.")

#main_4

if command == "1":
    country_name = input("Enter country name: ")
    distance = calculate_distance(current_location, country_name)
    need_fuel = fuel_consumed(distance)
    if user_fuel >= need_fuel:
        current_location = country_name
        user_fuel -= need_fuel
        print(f"You have arrived in {current_location}. Fuel remaining: {user_fuel:.2f} liters.")
    else:
        print("You don't have enough fuel to reach the destination!")

#main_final

print(f"You have enough weapons to rescue people in the last country: {final_location}. Lets go to Madrid.\n")
print(f"It takes you {final_weapon} weapons to complete the final mission")
print(f"Bravo! You have completed the final mission!\nYou got {final_reward} euros as a reward.\n")

# Update new location
pl.update_player(player, final_location)

# Calculate score
distance = cd.calculate_distance(current_location, final_location)
need_fuel = fc.fuel_consumed(distance)
player_money += final_reward
player_fuel -= need_fuel
player_weapon -= final_weapon
score = player_money + player_fuel*10 + player_weapon*10

# Get ranking info
ranking_info = rk.get_ranking_info(player_info[0])

# If there is no previous ranking info
# then add a new one, otherwise update it
if ranking_info is None:
    rk.add_ranking(player_info[0], score)
else:
    rk.update_player_score(player_info[0], score)

print(f"The game ends! You got {score} points totally.\n")

check_ranking = input("Would you like to see your rankings?(y/n)\n")
if check_ranking == "y":
    all_rankings = rk.get_all_player_ranking()
    for index, ranking in enumerate(all_rankings, start=1):
        if ranking[0] == player:
            print(f"{index}/ \033[1m{ranking[0]} {ranking[1]}\033[0m <-----Here is your ranking")
        else:
            print(f"{index}/ {ranking[0]} {ranking[1]}")