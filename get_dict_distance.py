import get_dict_airportcoordinate_by_country
import calculate_distance
def get_dict_distance(current_location):
    dict_distance = {}
    dict_airport_coordinate = get_dict_airportcoordinate_by_country(countries)
    for country in dict_airport_coordinate:
        distance = calculate_distance(current_location,country)
        dict_distance[country] = distance
    return dict_distance
dict_distance = get_dict_distance("Finland")
print(dict_distance)