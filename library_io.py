#!/usr/bin/env python
# Prerana Rout

import sys
import csv

# general
RED_TEXT="\033[31m"
GREEN_TEXT="\033[32m"
YELLOW_TEXT="\033[33m"
BLUE_TEXT="\033[34m"
NORMAL_TEXT="\033[00m"

def pprint(color, text):
	# print (color+text), NORMAL_TEXT
	print text#, "<br>"

# Reads CSV files
def read_csv(filename):
	csv_matrix_ = []
	
	with open(filename, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=",", quotechar="|")
		for row in csvreader:
			csv_matrix_.append(row)

	return csv_matrix_

def csv_to_1d_list(csv_matrix):
	var_list = []
	for i in csv_matrix:
		for j in i:
			if ((j == ' ') or (j == '')):
				continue
			x = float(j)
			x = int(x)
			if (x > 1):
				x = 1
			elif (x < 0):
				x = 0
			var_list.append(x)

	return var_list