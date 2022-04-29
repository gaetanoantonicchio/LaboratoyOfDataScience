# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 12:45:36 2021

@author: Gaetano
"""

import pyodbc
import csv

server = 'tcp:131.114.72.230'
database="Group_28_DB"
username="Group_28"
password="L1GGUHBQ"

connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()

# abbiamo splittato tournament in 3 partizioni 
for partition in range(3):
    tourn_file = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\split_tournament\tournament" + str(partition) + ".csv", "r")
    csv_file = csv.DictReader(tourn_file, delimiter = ",")
    
    sql_query = "INSERT INTO Tournament(tourney_id,date_id,tourney_name,surface,draw_size,tourney_level,tourney_spectators,tourney_revenue) VALUES (?,?,?,?,?,?,?,?)"
    i=1
    print("--->Loading partition number: " + str(partition))
    for row in csv_file:
        val = (row["tourney_id"], row["date_id"], row["tourney_name"], row["surface"],  row["draw_size"],\
               row["tourney_level"], row["tourney_spectators"], row["tourney_revenue"])
        cursor.execute(sql_query, val)
        print("Loading row %d" %i)
        i=i+1
    print("---> Finished loading partition number: "+ str(partition))
    tourn_file.close()
    cnxn.commit()
    print("Commit successful")
    

cursor.close()
cnxn.close()