# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 12:48:37 2021

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


geo_file = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\players.csv", "r")
csv_file = csv.DictReader(geo_file, delimiter = ",")

sql_query = "INSERT INTO Players(player_id,name,sex,hand,ht,country_id,byear_of_birth) VALUES (?,?,?,?,?,?,?)"
i=1
for row in csv_file:
    val = (row["player_id"], row["name"], row["sex"], row["hand"],  row["ht"],\
           row["country_id"], row["byear_of_birth"])
    cursor.execute(sql_query, val)
    print("Loading row %d" %i)
    i=i+1

geo_file.close()
cnxn.commit()
cursor.close()
cnxn.close()