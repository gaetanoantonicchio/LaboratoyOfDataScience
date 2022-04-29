# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 12:41:19 2021

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


date_file = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\date.csv", "r")
csv_file = csv.DictReader(date_file, delimiter = ",")

sql_query = "INSERT INTO Date(date_id,day,month,year,quarter) VALUES (?,?,?,?,?)"
i=1
for row in csv_file:
    val = (row["date_id"], row["day"], row["month"], row["year"],  row["quarter"])
    cursor.execute(sql_query, val)
    print("Loading row %d" %i)
    i=i+1

date_file.close()
cnxn.commit()
cursor.close()
cnxn.close()