#!/usr/bin/python

import os
import sys
import json


"""
Reads a file with a JSON file name. The JSON is in the following format:

- Dictionary that contains one nested hash and one list
- The hash is of pairs of names and ages (name is the key and age is be the value)
- The array is be a list of ages
"""
def read_json_from_file(filename):
	with open(filename, 'r') as file:
		return json.load(file)


"""
Writes output to file in expected format:
<age>-<larger age>
- :<name>

For all ages and names.
"""
def write_json_to_file(output_filename, output_json):
	with open(output_filename + ".yml", 'w') as file:
		for key in output_json.keys():
			file.write(key + "\n")
			for value in output_json[key]:
				file.write("- :" + value + "\n")


"""
Adds a zero to the beginning of a list if not contains a zero.
"""
def verify_zero_in_ages_list(ages_list):
	if 0 not in ages_list:
		ages_list.insert(0,0)


"""
Given a list of ages, adds the largets to ages_list, if not already inside.
"""
def add_oldest_age(ages_list, ppl_ages):
	max_age = max(ages_list)
	for age in ppl_ages.values():
		if age > max_age:
			max_age = age
	ages_list.append(max_age)


"""
Creates a dictionary output_json. Keys are "<age>-<next age>" from ages_list, value is a list containing all names from ppl_ages list whose age fits.
"""
def populate_dict(ages_list, ppl_ages):
	output_json = {}
	for i in range(len(ages_list) - 1):
		output_json[str(ages_list[i]) + "-" + str(ages_list[i+1])] = []
	for name, age in ppl_ages.items():
		for i in range(len(ages_list) - 1):
			if age >= ages_list[i] and age <= ages_list[i+1]:
				output_json[str(ages_list[i]) + "-" + str(ages_list[i+1])].append(name)
	return output_json


"""
Given a filename, returns the filename without the suffix.
"""
def  remove_filename_suffix(filename):
	return os.path.splitext(os.path.basename(filename))[0]


"""
Reads an input parameter with a JSON file name (for instance my_list.json). The JSON is be in the following format:

- Dictionary that contains one nested hash and one list
- The hash is of pairs of names and ages (name is the key and age is be the value)
- The array is be a list of ages

The program go over the list of people and divide them to buckets based on their ages. Each bucket holds all the names of the people with age between the partition key and the following partition key.
e.g. Bucket ‘20-25’ holds a list of name that their age is between 20 and 25 (not including). This data is saved in a yaml format in a file with the same name as the input file with changed extension.
If there is someone that doesn't fall into any of the baskets it creates a new bucket based on the oldest person and add all the people that fall into this bucket.
"""
def main(filename="a.txt"):
	input_json = read_json_from_file(filename)
	ages_list = input_json["buckets"]
	ages_list = sorted(ages_list)
	ppl_ages = input_json["ppl_ages"]

	verify_zero_in_ages_list(ages_list)
	add_oldest_age(ages_list, ppl_ages)

	output_json = populate_dict(ages_list, ppl_ages)
	output_filename = remove_filename_suffix(filename)
	write_json_to_file(output_filename, output_json)


if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		print("Usage: names-ages.py <filename>")
