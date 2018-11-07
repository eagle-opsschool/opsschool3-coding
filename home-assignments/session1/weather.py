#!/usr/bin/python

import sys
import requests
import json
import random

"""
Returns a tuple of the city and the country of the public ip of the host.
Exceptions happens in case of network errors, so may throws requests.exceptions.RequestException.
"""
def location_from_ip():
	location_json = json.loads(requests.get("http://ip-api.com/json").content)
	return (location_json["city"], location_json["country"])


"""
Given a city name and country name, returns a json dict of openweathermap weather information regarding said city and country.
Exceptions happens in case of network error, so may throws requests.exceptions.RequestException.
"""
def get_weather_from_location(city, country):
	return json.loads(requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + city + "," + country + "&appid=1e4e0972eaf38b44cddb624159132a3e").content)


"""
Transforms degrees from kelvin to celsius.
"""
def kelvin_to_celsius(degree):
	return degree-273.15


"""
Given a filename in current directory, weather json file and a country name, write weather inforamtion to filename.
Exceptions happens in case of IO errors, so may throws IOError.
"""
def write_weather_info_to_file(filename, weather, country_name):
	with open(filename, 'a') as file:
		file.write("The weather in " + str(weather["name"]) + ", " + country_name + " is " + str(kelvin_to_celsius(weather["main"]["temp"])) + " degrees.\n")


"""
Generate list of large cities and countries from a public repo in github.
Returns output in json.
Exceptions happens in case of network errors, so may throws requests.exceptions.RequestException.
"""
def generate_cities_list():
	cities_json = json.loads(requests.get("https://raw.githubusercontent.com/mahemoff/geodata/master/cities_with_countries.txt").content)
	return cities_json


"""
Selects and returns a random pair of country and city from a json file containing list of them.
"""
def get_random_city_country(cities_list):
	country_index = random.randint(0,len(cities_list) - 1)
	return (cities_list[country_index]["city"], cities_list[country_index]["country"])


"""
Checks computer's location according to IP. Then checks the current weather at found location and writes
the result to a file in a regular text format.
If argument is False, it creates a list with at least 10 cities, And prints their current weather in the following format:
“The weather in <city>, <country>(full country name) is XX degrees.

Paramters: tenCities (boolean). If true, output weather report for ten random large cities across the globe. Otherwise, uses geoIP to
find city in which the host IP is from, and output weather report for this city.
"""
def main(tenCities=True):
	weather = 0
	city = 0
	country = 0
	cities_list = 0
	filename = input("Please enter filename to write weather info into: ")
	if tenCities:
		try:
				cities_list = generate_cities_list()
		except requests.exceptions.RequestException as e:
			print("Error occurred connecting to the internet:")
			print(e)
			return 1
	for i in range(10):
		try:
			while True: #openweathermap sometimes doesn't recognise cities from generate_cities_list(), so trying until he does recognise.
				if tenCities:
					city, country = get_random_city_country(cities_list)
				else:
					city, country = location_from_ip()
				weather = get_weather_from_location(city, country)
				if weather["cod"] != "404": #If openweathermap didn't recognised, try again.
					break
		except requests.exceptions.RequestException as e:
			print("Error occurred connecting to the internet:")
			print(e)
			return 1
		try:
			write_weather_info_to_file(filename, weather, country)
		except IOError as e:
			print("Error occourred writing to file:")
			print(e)
			return 1
		if not tenCities:
			return 0

if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1] == "False":
		main(False)
	else:
		main()
