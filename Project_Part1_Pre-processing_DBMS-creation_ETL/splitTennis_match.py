# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 14:52:26 2021

@author: Gaetano Antonicchio, Gloria Segurini

Assignment 1:
    split tennis.csv
    Creazione match.csv
"""
import csv

tennis = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\tennis.csv", "r")
tennis_out = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\tennis_out.csv", "w")

#########################################
#  LEGEND --> Map col-index di tennis:  #
#########################################

# 'tourney_id': 0, 'tourney_name': 1, 'surface': 2, 'draw_size': 3, 'tourney_level': 4,
# 'tourney_date': 5, 'match_num': 6, 'winner_id': 7, 'winner_entry': 8, 'winner_name': 9,
# 'winner_hand': 10, 'winner_ht': 11, 'winner_ioc': 12, 'winner_age': 13, 'loser_id': 14, 
# 'loser_entry': 15, 'loser_name': 16, 'loser_hand': 17, 'loser_ht': 18, 'loser_ioc': 19,
# 'loser_age': 20, 'score': 21, 'best_of': 22, 'round': 23, 'minutes': 24, 'w_ace': 25, 'w_df': 26,
# 'w_svpt': 27, 'w_1stIn': 28, 'w_1stWon': 29, 'w_2ndWon': 30, 'w_SvGms': 31, 'w_bpSaved': 32,
# 'w_bpFaced': 33, 'l_ace': 34, 'l_df': 35, 'l_svpt': 36, 'l_1stIn': 37, 'l_1stWon': 38, 'l_2ndWon': 39,
# 'l_SvGms': 40, 'l_bpSaved': 41, 'l_bpFaced': 42, 'winner_rank': 43, 'winner_rank_points': 44,
# 'loser_rank': 45, 'loser_rank_points': 46, 'tourney_spectators': 47, 'tourney_revenue': 48

##############################################################################
#      MODIFICO TENNIS.CSV IN MODO DA PREPARARLO PER SCRIVERE MATCH          #
##############################################################################

# Scrivo l'header
first = True
for row in tennis.readlines():
    token = row.strip().split(',')
    if first:
        token.append('match_id')         
        for i in range(len(token)):
            if i == len(token)-1:
                tennis_out.write(token[i]+'\n')
            else:
                tennis_out.write(token[i]+',')           
        first=False
    # Scrivo le righe
    else:
        # match_num + toureny_id + tourney_name + '-' + tourney_level
        token.append(token[6]+ token[0] +token[1].strip().lower() +'-'+token[4].upper()) 
        for i in range(len(token)):
            if i == len(token)-1:
                tennis_out.write(token[i]+'\n')
            else:
                if i == 0: #tourney_id
                    tennis_out.write(token[i]+ token[1].strip().lower() + token[4].upper() + ',')  #token[4] is tourney_level
                else:
                    tennis_out.write(token[i]+',')
tennis.close()
tennis_out.close()

###############################################################################
# Attributi da scrivere sul file match.csv
col2write = ['match_id','tourney_id','winner_id','loser_id','score', 'best_of',
             'round', 'minutes','w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon',
             'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df', 'l_svpt',
             'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved','l_bpFaced', 'winner_rank',
             'winner_rank_points', 'loser_rank', 'loser_rank_points','winner_name', 'loser_name']


###############################################################################
#         SCRIVO MATCH.CSV  - QUESTO FILE CONTIENE DEI DUPLICATI              #
###############################################################################

match = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\match_beta.csv", "w")
tennis = csv.DictReader(open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\tennis_out.csv","r"))

# Scrivo l'header
for i in range(len(col2write)):
    if i == len(col2write)-1:
        match.write(col2write[i]+'\n')
    else:
        match.write(col2write[i]+',')
# Scrivo i valori
for row in tennis:        
    for i in range(len(col2write)):
        # se è l'ultima colonna
        if i == len(col2write)-1:
            # appendi il valore e inizia una nuova riga
            match.write(row[col2write[i]] +'\n')
        else:
            match.write(row[col2write[i]]+ ',')
match.close()

##############################################################################
# ELIMINAZIONE DUPLICATI E RISOLUZIONE PROBLEMA MATCH DIVERSI CON STESSO ID  #
##############################################################################

visited_rows = set()
rows2write = set()
visited_id = set()

with open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\match_beta.csv", "r") as match_in:
    with open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\match.csv", "w") as match_out:
        for row in match_in.readlines():
            token = row.strip().split(',')
            # se il match_id non è in visited
            if token[0] not in visited_id:
                # aggiungo l'id a visited
                visited_id.add(token[0])
                # aggiungo la riga a visited rows
                visited_rows.add(tuple(token))
                # scrivo la riga sul file match_out
                match_out.write(row)
            
            # se il match_id è presente in visited
            elif token[0] in visited_id:
                # se la riga non è in visisted_rows --> quindi è diversa, non è un duplicato
                if tuple(token) not in visited_rows:
                    # aggiungila a row2write
                    rows2write.add(tuple(token))                

# problema dei match diversi con stesso ID 
# itero sulle rows2write, e aggiungo al match_id un numero sequenziale in modo tale
# da rendere unica la chiave match_id 
 
with open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\match.csv", "a") as match:
          # inizializzo numero da aggiungere a match_id
          num = 0
          for row in rows2write:
              # stringa che verrà scritta sul file
              line=""
              for i in range(len(row)):
                # se la col è match_id
                if i == 0:
                      line+= str(row[0]) +'-'+ str(num)+","
                      num+=1
                else:
                    # altrimenti se sono attriuti diversi da match_id aggiungili normalmente
                    line+=row[i]+","   
              # scrivi line sul file match_out.csv      
              match.write(line[:-1] + '\n') 
             
