#!/usr/bin/python3

###########################################
# This file generates the statistics 
# over the students attendency of a 
# given semester.
# IMPORTANT: change the stat_path variable
# to have the correct path to the students 
# folder. 
# Authors: Andrii Sokolov, Elena Blokhina.
###########################################

from os import listdir

# THE FOLDER WITH ALL *.csv FILES! CHANGE IT!
stat_path = "/home/cbapka/MEGA/Attendance" 

names = listdir(stat_path)
print(names)
import pandas as pd 

dict_of_attendance = {}

main_file = open("students.csv")
for line in main_file:
	temp = line.split(",")
	dict_of_attendance[temp[0].upper()] = []

dates = []

for filename in names:
	if(filename[:4] == '2019'):
		for element in dict_of_attendance.keys():
			dict_of_attendance[element].append(0)
		dates.append(filename)
		date_file = open(filename)
		for line in date_file:
			print(filename)
			dict_of_attendance[line[:len(line)-1].upper()][-1]+=1

df = pd.DataFrame.from_dict(dict_of_attendance, orient='index',columns=dates)
df.to_csv("report.csv")
print(df)