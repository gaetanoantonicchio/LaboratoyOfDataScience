# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 16:24:17 2021

@author: Gaetano Antonicchio, Gloria Segurini
Script preprocessing match.csv e players.csv

"""
import pandas as pd
#import numpy as np

# carico i dataset
t = pd.read_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\tennis.csv") #tennis
to = pd.read_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\tournament.csv") # tournament
p = pd.read_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\players.csv") #players
m = pd.read_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\match.csv") #match
d = pd.read_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\date.csv") #date

########################################################################
# Player con altezza 2 cm viene considerato come NAN
########################################################################
# kamilla rakhimova 
p.loc[p['ht'] == 2] = 173.0

# Rimuovo col con + del 50% di missing values 
m.drop(columns=['minutes', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon',
       'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df',
       'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved',
       'l_bpFaced'], axis=1, inplace=True)


# Sostituisco i NAN in winner_rank e loser_rank utilizzando la media dei rank per quel
# giocatore calcolata in base all'anno a cui il rank si riferisce.

# faccio una join tra match (m), tournament (t) e date(d) in modo tale da avere informazioni 
# relative all'anno per ogni match.
mer_m = m.merge(to, on ='tourney_id').merge(d, on='date_id')

# rimpiazzo i missing values
m['winner_rank'] = mer_m.groupby(['year','winner_id'])['winner_rank'].transform(lambda x: x.fillna(x.mean()))
m['loser_rank'] = mer_m.groupby(['year','loser_id'])['loser_rank'].transform(lambda x: x.fillna(x.mean()))

###############################################################################
#             PER OGNI GIOCATORE OMONIMO CON ID DIVERSI                       #
#               CONTROLLO SE HA GIOCATO DEI MATCH                             #
###############################################################################
 
# raggruppo i giocatori in base al nome per vedere quali hanno più di un player_id
groupby_name = (p.groupby('name').count()[['player_id']] >1)
# quelli che hanno più di un player_id avranno come risultato True, mi salvo questi in una lista player_err
player_err = groupby_name[groupby_name['player_id']==True].index.tolist()

for pl in player_err:
    #salvo id associati al player pl
    id1 = p[p['name']==pl]['player_id'].iloc[0] 
    id2 = p[p['name']==pl]['player_id'].iloc[1]
    
    # controllo id1 in winner_id e loser_id
    # se non esiste un record in match di quel giocatore con id1 
    if m[m['loser_id']== id1].shape[0] == 0 and m[m['winner_id']== id1].shape[0] == 0:
        # rimuovo player in players.csv con id1
        p.drop(p[p['player_id'] == id1].index, inplace=True)
       
    # controllo id2 in winner_id e loser_id
    # se non esiste un record in match di quel giocatore con id2 
    if  m[m['loser_id']== id2].shape[0] == 0 and m[m['winner_id']== id2].shape[0] == 0:     
        p.drop(p[p['player_id'] == id2].index, inplace=True) 
        

# Stampa giocatori in players per vedere chi è stato eliminato.     
#for pl in player_err:
#    print(p[p['name']==pl])   # de-commenta per visualizzare i giocatori omonimi 
        
# Aggiusto Manualmente i giocatori omonimi.
# ALcuni giocatori sono stati duplicati con chiavi diverse, e dato che questi hanno giocato 
# partite con id diversi, vado in match ad aggiustare le chiavi manualmente.

""" Giocatori che sono da eliminare dopo aver effettuato un controllo manuale """
# Valentina Lia - 239415 da eliminare da players --- sostituire in match, l id 220334
# Stanislava Bobrovnikova - 225865 da eliminare --- sostituire 221347
# Nana Kawagishi 244078 da eliminare -- sostituire 221771
# Maria Fernanda Navarro 223287 da eliminare -- sostituire 223367
# Liisa Varul 222915 da eliminare -- sostituire 222914
# Lara Onal 223215 da eliminare -- sostituire 224486  
# Hei Ching Claudia Ng 219835 da eliminare -- sostituire 216586  
# Eleni Fasoula  222943  KAZ non esiste -- sostituire 222942  
# Ekaterina Makarova 223126  da eliminare -- sostituire 201505  
# Astrid Cirotte 223401   da eliminare -- sostituire 236980  
# Sofia Nahiara Garcia 236977 da eliminare -- sostituire 220928
# Holly Fisher 222228 da eliminare -- sostituire 221142  
# Guy Stockman 207142  da elminare -- sostituire 206883  
# Giuseppe Tresca 206834   da eliminare -- sostituire 207982  
# Fitriani Sabatini 239429   da eliminare -- sostituire 221189 
# Emilse Lujan Ruiz 236974 da eliminare -- sostituire 222646  
# Ellie Myers 240168   da eliminare -- sostituire 222407  

# rimuovo da players.csv i giocatori duplicati e non esistenti
player_id2drop = [239415, 225865, 244078, 223287, 222915, 223215, 219835,\
                  222943, 223126, 223401, 236977, 222228,207142, 206834,\
                  239429, 236974, 240168]

for p_id in player_id2drop:
    p.drop(p[p['player_id'] == p_id].index, inplace=True)

################ Sistemo i giocatori di players.csv ##########################
# Alcuni di questi giocatori avevano NAN o valori errati - Questi sono stati sistemati
# manualment

# Kuan Yi Lee - ci sono un uomo e una donna. Sistemo la giocatrice
p.loc[p['player_id']==221745, 'sex'] = 'F'
p.loc[p['player_id']==221745, 'ht'] = 178.0

# Matylda Burylo - norway & poland -- sono entrambe del 2004
p.loc[p['player_id']==222066, 'byear_of_birth'] = 2004.0
p.loc[p['player_id']==222845, 'byear_of_birth'] = 2004.0

# Eleni fasoula
p.loc[p['player_id']==222942, 'byear_of_birth'] = 2002.0

# astrid cirotte fix anno
p.loc[p['player_id']==236980, 'byear_of_birth'] = 2004.0

# maria fernanda navarro
p.loc[p['player_id']==223367, 'byear_of_birth'] = 1996.0

#Emilse Lujan Ruiz
p.loc[p['player_id']==222646, 'byear_of_birth'] = 2004.0

# Rimappo correttamente le chiavi in match, in modo tale che puntino allo stesso giocatore
correct_ids = [220334, 221347, 221771, 223367, 222914, 224486, 216586, 222942, 201505, 236980,220928, 221142,\
              206883, 207982,221189, 222646, 222407]
for wrong_id, right_id in zip(player_id2drop, correct_ids):
    # Sistemo gli id in match per players duplicati e eliminati
    m.loc[m['loser_id']== wrong_id, 'loser_id'] = right_id
    m.loc[m['winner_id']== wrong_id, 'winner_id'] = right_id        

###############################################################################
#      IMPORTO I SET MALE E FEMALE --> SERVONO PER DETERMINARE IL SEX       #
###############################################################################
from splitTennis_players import male, female  
      
###############################################################################
#          RISOLVO PROBLEMA DI PLAYERS DIVERSI CON LO STESSO ID               #
###############################################################################

# dizionario di tennis.csv con chiave: COL e valore: INDICE COL
i = {}
# dizionario in cui salvo per ogni chiave (player_id) una set di players name associati a quell'id
dic = {}
# set in cui salvo players che condividono il player_id con altri players
pdouble = set()

with open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\tennis.csv", 'r') as t:
    # GENERO DIZIONARIO PER INDICI DELLE COLONNE ---> QUESTO PER HEADER DI TENNIS.CSV
    first = True
    lines = t.readlines()
    for row in lines:
        tok = row.strip().split(',')
        if first:
            for idx, col in enumerate(tok):
                i[col] = idx
            first=False
        
        # AGGIUNGO ID COME CHIAVE E NOMI COME VALORI
        else:
            if tok[i['winner_id']] not in dic.keys():
                dic[tok[i['winner_id']]] = set()
                dic[tok[i['winner_id']]].add(tok[i['winner_name']])
            else:
                dic[tok[i['winner_id']]].add(tok[i['winner_name']])
           
    for row in lines:
        tok = row.strip().split(',')
        if first:
            continue
        else:
            if tok[i['loser_id']] not in dic.keys():
                dic[tok[i['loser_id']]] = set()
                dic[tok[i['loser_id']]].add(tok[i['loser_name']])
            else:
                dic[tok[i['loser_id']]].add(tok[i['loser_name']])
                
    # PER QUELLI CHE HANNO PIU DI DUE VALORI (NOMI) 
    for key, val in dic.items():
        if len(val) >1:
            for name in val:
                if name != 'Alena Fomina':
                    pdouble.add(name)

InPlayers = p['name'].tolist() # prendo nomi dei players da players.csv           

# differenza tra i giocatori che condividono un id e quelli che ho in players.
# il risultato di p2add sono i giocatori che devono essere inseriti con nuovi id generati
p2add = pdouble- set(InPlayers)

# ultimo player_id usato --> il massimo
max_playerId = max(p['player_id'])

# output --> è una lista di liste con le righe da appendere infondo al file players.csv
row2write = []
# serve per tenere traccia dei players per i quali ho già preso la riga che mi interessava
visited_names = set()

new_id = max_playerId

first = True
for row in lines:  # scorro tennis.csv
    tok = row.strip().split(',')
    # skip header
    if first:
        first = False
    for name in p2add:
        if name == tok[i['winner_name']]:
            if name not in visited_names:
                visited_names.add(name)
                new_id +=1
                line = [new_id, name.strip(), '', tok[i['winner_hand']], tok[i['winner_ht']], tok[i['winner_ioc']]]
                
                # fix hand 'U'
                if tok[i['winner_hand']] == 'U':
                    line[3] = ''  
                      
                # add sex
                if name in male:
                    line[2] = 'M'
                elif name in female:
                    line[2] = 'F'
                row2write.append(line)
                
                # add byear_of_birth
                if tok[i['winner_age']] != '': 
                    byear_of_birth = int(tok[i['tourney_date']][:4]) - int(float(tok[i['winner_age']]))
                    line.append(byear_of_birth)
                else:
                    line.append('')
            else: continue
               
        elif name == tok[i['loser_name']]:
            if name not in visited_names:
                visited_names.add(name)
                new_id +=1
                line = [new_id, name.strip(), '', tok[i['loser_hand']], tok[i['loser_ht']], tok[i['loser_ioc']]]
                 
                # fix hand 'U'
                if tok[i['loser_hand']] == 'U':
                    line[3] = ''
                    
                # add sex
                if name in male:
                    line[2] = 'M'
                elif name in female:
                    line[2] = 'F'
                    
                # add byear_of_birth
                if tok[i['loser_age']] != '': 
                    byear_of_birth = int(tok[i['tourney_date']][:4]) - int(float(tok[i['loser_age']]))
                    line.append(byear_of_birth)
                else:
                    line.append('')    
                row2write.append(line)
            else: continue  

###############################################################################
#                 SISTEMO I PLAYER_ID IN MATCH.CSV                            #
###############################################################################

for row in row2write:
    player_name = row[1]
    id_new = row[0]
    # aggiusto il winner_id/loser_id in match
    m.loc[m['loser_name']== player_name, 'loser_id'] = id_new
    m.loc[m['winner_name']== player_name, 'winner_id'] = id_new   

# rimuovo col: winner_name, lose_name - queste sono state usate per modificate il winner e loser id
m = m.iloc[:,:-2]
# scrivo match
m.to_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\match.csv", sep=',', header=True, index=False)
# scrivo players per mantenere le modifiche fatte fin ora
p.to_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\players.csv", sep=',', header=True, index=False)

###############################################################################
#          AGGIUNGO PLAYERS MANCANTI CON NEW ID A PLAYERS.CSV                 #
###############################################################################

with open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\players.csv", "a+") as players:
    for row in row2write:
        line = str()
        for i in range(len(row)):
            if i == len(row)-1:
                line += str(row[i]) +'\n'
            else:
                line += str(row[i]) + ','
        players.write(line)
         
##### 
# REPLACE MISSING VALUES ##########################
### HT #####

players = pd.read_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\players.csv")
geo = pd.read_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\geography.csv")

players.loc[players['player_id'] == 200707, 'sex' ] = 'M'
players.loc[players['player_id'] == 209890, 'sex' ] = 'M'
players.loc[players['player_id'] == 209404, 'sex' ] = 'M'
players.loc[players['player_id'] == 209984, 'sex' ] = 'M'

merged_df = players.merge(geo, on='country_id')
merged_df['ht'] = merged_df['ht'].astype(float)

# compute average ht for males by continent
ht_M = merged_df[merged_df['sex']=='M'].groupby('continent').mean()[['ht']]
ht_M = round(ht_M['ht'])
# replace missing values
df_M = merged_df[merged_df['sex']=='M'].merge(ht_M, on='continent')
df_M['ht_x'].fillna(df_M['ht_y'], inplace=True)
# male dataframe with replaced missing values
df_M = df_M.iloc[:,:-1] 

# compute average ht for females by continent
ht_F = merged_df[merged_df['sex']=='F'].groupby('continent').mean()[['ht']]
ht_F = round(ht_F['ht'])

#replace missing values
df_F = merged_df[merged_df['sex']=='F'].merge(ht_F, on='continent')
df_F['ht_x'].fillna(df_F['ht_y'], inplace=True)
# male dataframe with replaced missing values
df_F = df_F.iloc[:,:-1] 

#join df_F and df_M to obtain players with replaced missing values
frames = [df_M, df_F]
players = pd.concat(frames)
# fix col name for ht
players.rename(columns= {'ht_x':'ht'}, inplace=True)

# aggiusto giocatore alto 145.00 cm - Ilija Vucic
players.loc[players['player_id'] ==105661, 'ht'] = 188.00


##### HAND ########
# rimpiazzo i NaN con la moda
players['hand'].fillna(players['hand'].mode()[0], inplace=True)

# Rimuovo language e continent da players. Queste col erano state aggiunte dopo il merge con geography
players = players.iloc[:,:len(players.columns)-2]

# SCRIVO IL CSV PLAYERS


#aggiusto i data types
players['player_id'] = players['player_id'].astype(int)
players['byear_of_birth'].fillna(-1, inplace=True)
players['byear_of_birth'] = players['byear_of_birth'].astype(int)
players.drop_duplicates(inplace=True)
players['name'] = players['name'].str.strip()
players.to_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\players.csv",sep=',', header=True, index=False)

with open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\players.csv", "a") as pl:
    pl.write("215872,Kamilla Rakhimova,F,R,173.0,RUS,2001\n")
    
###############################################################################
# PREPROCESSING TOURNAMENT.CSV - RIMPIAZZO I MISSING VALUES IN SURFACE        #
###############################################################################

tournament = pd.read_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\tournament.csv")

# Rimpiazzo i Missing values in surface 62 rows.
# Usiamo la moda --> HARD
tournament.fillna(tournament['surface'].mode()[0], inplace=True)

# Scrivere modifiche su file
tournament.to_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\tournament.csv", sep=',', header=True, index=False)

        
        