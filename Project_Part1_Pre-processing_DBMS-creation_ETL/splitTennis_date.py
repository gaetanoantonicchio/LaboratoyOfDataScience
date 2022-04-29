# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 16:54:21 2021

@author: Gaetano Antonicchio, Gloria Segurini
    split tennis.csv
    Creazione date.csv
"""
import csv

tennis = csv.DictReader(open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\tennis.csv", "r"))

day =[]
month =[]
year =[]
quarter =[]

already_visited = [] #avoid duplicate rows
var = 'tourney_date'

for r in tennis: 
    if r[var] not in already_visited:
        already_visited.append(r[var])
        year.append(r[var][:4])
        mth = int(r[var][4:6])
        month.append(str(mth))
        if  mth >= 1 and mth<=3:
            quarter.append('Q1')
        elif mth >3 and mth<=6:
            quarter.append('Q2')
        elif mth >6 and mth <=9:
            quarter.append('Q3')
        else:
            quarter.append('Q4')
        day.append(r[var][6:])
              
date = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\date.csv", "w")
date.write('date_id'+','+'day'+','+'month'+','+'year'+','+'quarter'+'\n')
for date_id, d, m, y, q in zip(already_visited,day,month,year,quarter):
    date.write(str(date_id) +','+d+','+m+','+y+','+q+'\n')
