#!/usr/bin/python3

##################################################
# This script registers the atendency of students
# using their NFC codes of the UCD U-cards.
# It creates the csv files for every date. The first
# registration includes the database creation with
# manual student's logging :(
# Authors: Andrii Sokolov, Elena Blokhina
##################################################

import nfc
from nfc.clf import RemoteTarget
import curses
import os
from datetime import date

def read_tag():
    clf = nfc.ContactlessFrontend()
    assert clf.open('usb') is True
    ans = ''
    while True:
        target = clf.sense(RemoteTarget('106A'))
        if (str(target)!='None'):
            ans = str(target)
            break
    clf.close()
    ans = ans.split(" ")
    return(ans[1][8:])

def read_initial_file():
    students_file = open("students.csv","r")
    students = dict([])
    for line in students_file:
        #print(line)
        temp = line.split(',')
        students[temp[1][:len(temp[1])-1]] = temp[0]
    return(students)

def initial_file():
    students_list = dict([])
    try:
        students_list = read_initial_file()
    except:
        file = open("students.csv",'w')
        file.close()
    while(True):
        in_Name = input("Enter the Name:")
        if (str(in_Name) == 'exit'):
            break
        else:
            try:
                students_list = read_initial_file()
            except:
                print('ERROR!')
            export_file = open("students.csv","a")
            print("Tag: ")
            tag = read_tag()
            #print(students_list)
            if(in_Name in students_list.values()):
                print("Student with this name is already exist! ")
            elif(tag in students_list):
                print("Student with the same card is already exist")
            else:
                export_file.write(str(in_Name)+",")
                export_file.write(tag+"\n")
                export_file.close()


def read_today_file():
    ans = []
    try:
        attendance = open(str(date.today())+'.csv','r')
        for line in attendance:
            ans.append(line[:len(line)-1])
    except:
        pass
    return(ans)

def tag_attendance():
    students = read_initial_file()
    attend_stud = read_today_file()
    while(True):
        try:
            key = input('Command or Enter for the reading:')
            if key == ('exit'):
                break
            else:
                tag = read_tag()
                if tag in students:
                    if students[tag] not in attend_stud:
                        attendance = open(str(date.today())+'.csv','a')
                        attend_stud.append(students[tag])
                        attendance.write(students[tag]+'\n')
                        attendance.close()
                        print(students[tag]+' Successfully added!')
                    else:
                        print(students[tag]+' Already added!')
                else:
                    key2 = input('Add this student to the list? (y/n) ')
                    if (key2 == 'y'):
                        export_file = open("students.csv","a")
                        name = input('Enter the Name: ')
                        export_file.write(str(name)+','+str(tag)+'\n')
                        export_file.close()
                        attend_stud.append(name)
                        students[tag]=name
                        attendance = open(str(date.today())+'.csv','a')
                        attendance.write(name+'\n')
                        attendance.close()
                    else:
                        print('Students attendance did not taken into account!')
        except:
            pass

key = input('Press 1 to REWRITE student-tag file, or Enter to read tags for today: ')
if (key == '1'):
    initial_file()
else:
    tag_attendance()
