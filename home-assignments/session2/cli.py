#!/usr/bin/python3

import re
import click
from weather import Weather, Unit


def validate_input_forecast(forecast):
	if not re.match("^TODAY(\+\d+)?$", forecast):
		print("--forecast flag must get 'TODAY' or 'TODAY+<num>' where <num> is number of days for weather forecast.")
		exit(1)


def validate_input_city(city_weather_info, city):
	if not city_weather_info:
		print("Cannot find a weather forecast for " + city + ".")
		exit(1)


def get_number_of_days(forecast):
	if forecast.upper() == "TODAY":
		return 0
	return int(forecast[len("TODAY+"):])


def print_weather_forecast(city, city_weather_info, extra_days, units):
	if extra_days == 0:
		print("The weather in " + city + " today is " + city_weather_info.condition.text + " with temperatures trailing from " +
			city_weather_info.print_obj["item"]["forecast"][0]["low"] + "-" + city_weather_info.print_obj["item"]["forecast"][0]["high"] + " " + units.lower() + ".")
	else:
		for i in range(min(extra_days, len(city_weather_info.print_obj["item"]["forecast"]))):
			print(city_weather_info.print_obj["item"]["forecast"][i]["date"] + " " + city_weather_info.print_obj["item"]["forecast"][i]["text"] + " with temperatures trailing from " +
				city_weather_info.print_obj["item"]["forecast"][i]["low"] + "-" + city_weather_info.print_obj["item"]["forecast"][i]["high"] + " " + units.lower() + ".")


@click.command()
@click.option('--city', help='City name.')
@click.option('--forecast', help='TODAY or TODAY+<num> where <num> is number of days for weather forecast.')
@click.option('-f', 'units', flag_value='FAHRENHEIT', help="Show temperatures in Fahrenheit. Note: cannot also choose -c")
@click.option('-c', 'units', flag_value='CELSIUS', default=True, help="Show temperatures in Celsius. Note: cannot also choose -f")
def main(city, forecast, units):
	weather = Weather(unit=getattr(Unit, units))
	validate_input_forecast(forecast)

	city_weather_info = weather.lookup_by_location(city)
	validate_input_city(city_weather_info, city)

	extra_days = get_number_of_days(forecast)
	print_weather_forecast(city, city_weather_info, extra_days, units)


if __name__ == '__main__':
	main()
