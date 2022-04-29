# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 17:09:14 2021

@author: Gaetano Antonicchio, Gloria Segurini
"""
import csv

tennis = csv.DictReader(open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\tennis_out.csv", "r"), delimiter=',')
col2write = ['tourney_id', 'date_id', 'tourney_name', 'surface', 'draw_size',
             'tourney_level', 'tourney_spectators', 'tourney_revenue']
tournament = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\tournament_beta.csv", "w")

# tournament_beta includerà duplicati che saranno rimossi in uno step successivo
# scrivo header
for i in range(len(col2write)):
    if i == len(col2write)-1:
        tournament.write(col2write[i]+'\n')
    else:
        tournament.write(col2write[i]+',')

for row in tennis:
    for i in range(len(col2write)):
        if i == len(col2write)-1:
            tournament.write(row[col2write[i]]+'\n')
        else:
            if col2write[i] == 'tourney_id':
                # il tourney_id è stato già modificato correttamente su tennis
                # come concatenazione di tourney_id + tourney_name + tourney_level
                tournament.write(row[col2write[i]] + ',') 
            elif col2write[i] == 'date_id':
                tournament.write(row['tourney_date']+',')
            else:
                tournament.write(row[col2write[i]]+',')
tournament.close()

# Eliminate duplicate rows from tounrnament
with open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\tournament_beta.csv", "r") as tournament_in,\
        open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\tournament.csv", 'w') as tournament_out:

    seen = set()  # set per lookup
    for line in tournament_in.readlines():
        token = line.strip().split(',')
        # se il tourney_id è in seen
        if token[0] in seen:  
            continue  # skip duplicato
        seen.add(token[0])
        tournament_out.write(line)
tournament_in.close()
tournament_out.close()




