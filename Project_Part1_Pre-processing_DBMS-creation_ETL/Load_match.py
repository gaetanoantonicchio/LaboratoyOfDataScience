# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 12:50:24 2021

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

for partition in range(62):
    match_file = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\split_match\match"+ str(partition) +".csv", "r")
    csv_file = csv.DictReader(match_file, delimiter = ",")
    
    sql_query = "INSERT INTO Match(match_id,tourney_id,winner_id,loser_id,score,best_of,round,winner_rank,winner_rank_points,loser_rank,loser_rank_points) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
    i=1
    print("--->Loading partition number: " + str(partition))
    for row in csv_file:
        val = (row["match_id"], row["tourney_id"], row["winner_id"], row["loser_id"],  row["score"],\
               row["best_of"], row["round"], row["winner_rank"], row["winner_rank_points"], row["loser_rank"], row["loser_rank_points"])
        cursor.execute(sql_query, val)
        print("Loading row %d" %i)
        i+=1
    print("---> Finished loading partition number: "+ str(partition))
    match_file.close()
    cnxn.commit()
    print("Commit successful")
    
cursor.close()
cnxn.close()