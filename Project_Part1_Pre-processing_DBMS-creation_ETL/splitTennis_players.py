# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 17:06:00 2021

@author: Gaetano 
SPLIT Players
"""
male_ply = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\male_players.csv", "r")
female_ply_in = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\female_players.csv", "r")
tennis = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\tennis.csv", "r")

# dizionario in cui salvo --> chiave: nome del player, valore: sex
players = dict()

# salvo nomi dei players male e female
male = set()
female = set()

###############################################################################
#    PULISCO MALE E FEMALE PLAYERS, RIMUOVENDO GIOCATORI INESISTENTI          #
###############################################################################

" Preprocessing di Female_players.csv "
skip = True
for row in female_ply_in:
    if skip:
        skip = False
    else:
        r = row.strip().split(',')
        # se il nome è Unknown, '' e il cognome è Unknown o ''
        if (r[0] == 'Unknown' or r[0] == '') and (r[1] == '' or r[1] == 'Unknown'):
            continue
        # se il nome è diverso da Unknown e da '' e il cognome è Unknown o ''
        elif (r[0] != 'Unknown' or r[0] != '') and (r[1] == '' or r[1] == 'Unknown'):
            # prendi solo il nome 
            name = str(r[0])
            female.add(name.strip())
            players[name] = 'F'
        
        # se il nome è Unknown o '' e il cognome è diverso da Unknown o ''
        elif (r[0] == 'Unknown' or r[0] == '') and (r[1] != 'Unknown' or r[1] != ''):
            # prendi solo il cognome
            name = str(r[1])
            female.add(name.strip())
            players[name] = 'F'
            
        # se il nome e il cognome sono diversi da Unknown o ''
        elif (r[0] != 'Unknown' or r[0] != '') and (r[1] != 'Unknown' or r[1] != ''):
            # il name è la concatenazione di nome+cognome
            name = str(r[0]+' '+r[1])
            # eccezione di questo caso anomalo 
            if name == 'X, X':
                continue
            else:
                female.add(name.strip())
                players[name] = 'F'

" Pre-processing di Male_players.csv "
skip = True
for row in male_ply:
    if skip:
        skip = False
    else:
        r = row.strip().split(',')
    if (r[0] == 'Unknown' or r[0] == '') and (r[1] == '' or r[1] == 'Unknown'):
        continue
    elif (r[0] != 'Unknown' or r[0] != '') and (r[1] == '' or r[1] == 'Unknown'):
        name = str(r[0])
        male.add(name.strip())
        players[name] = 'M'
    elif (r[0] == 'Unknown' or r[0] == '') and (r[1] != 'Unknown' or r[1] != ''):
        name = str(r[1])
        male.add(name.strip())
        players[name] = 'M'
    elif (r[0] != 'Unknown' or r[0] != '') and (r[1] != 'Unknown' or r[1] != ''):
        name = str(r[0]+' '+r[1])
        male.add(name.strip())
        players[name] = 'M'

# Controllo se ci sono players che sono erroneamente sia in Male che Female
intersection = female.intersection(male)

# In fixed salvo il nome dei players per i quali siamo riusciti ad sistemare il sex
fixed = set()

lines = tennis.readlines()
# sistema il sex dei giocatori presenti in intersection
for name in intersection:
    for row in lines:
        token = row.strip().split(',')
        # se nome = winner_name  e loser_name non sta in intersection (quindi ha il sex corretto)
        if name == token[9] and token[16] not in intersection:
            # il giocatore con sesso dubbio avrà lo stesso sex del suo avversario
            players[token[9]] = players[token[16]]
            # aggiungi il player a fixed per tenerne traccia
            fixed.add(name)
            break # una volta sistemato non deve scorrere tutte le righe di tennis
            
        # se nome = loser_name e winner_name non sta in intersection (quindi ha il sex corretto)
        elif name == token[16] and token[9] not in intersection:
            # il giocatore con sesso dubbio avrà lo stesso sex del suo avversario
            players[token[16]] = players[token[9]]
            # aggiungi il player a fixed per tenerne traccia
            fixed.add(name)
            break

" Stampa per vedere risultati intermedi - Debugging"
#print(intersection)
#print(fixed)        
#print('num of players in dict before cleaning ', len(players.keys()) )
#print('fixed: ',len(fixed), 'out of ', len(intersection))


# In players2remove individuo i players per i quali non siamo riusciti a risalire al sex
players2remove = intersection - fixed
for name in players2remove:
    # li cancelliamo da players
    del players[name]

#print('num of players in dict after cleaning', len(players.keys()) )
tennis.close()

####################################################################################
#    PRENDO LE RIGHE DEI WINNERS E LOSERS DA TENNIS PER SCRIVERE IL FILE PLAYERS   #
####################################################################################

tennis = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\tennis.csv", "r")
lines = tennis.readlines()

# salvo una lista di liste contenente la riga con gli attributi di ogni winner
winners = []
# salvo i nomi dei winners 
w_names = set()
# salvo una lista di liste contenente la riga con gli attributi di ogni loser
losers = []
# salvo i nomi dei losers
l_names=set()
# dizionario in cui salvo il nome delle col di tennis e il relativo indice
# usato per rendere più leggibile il codice
i = dict()

first = True
for row in lines: # per ogni riga in tennis
     r = row.strip().split(',')
     if first:
         # creo dizionario col - index di tennis.csv
         for index_col, col_name in enumerate(r):
             i[col_name] = index_col
         first=False 
     else:
        r = row.strip().split(',')
        # index, col: 0 data, 1 name, 2 id, 3 hand, 4 ht, 5 country_id, 6 age
        winners.append([r[i['tourney_date']], r[i['winner_name']], r[i['winner_id']],\
                        r[i['winner_hand']], r[i['winner_ht']], r[i['winner_ioc']], r[i['winner_age']]]) 
        w_names.add(r[i['winner_name']])
        
        losers.append([r[i['tourney_date']], r[i['loser_name']],r[i['loser_id']],\
                        r[i['loser_hand']],r[i['loser_ht']],r[i['loser_ioc']],r[i['loser_age']]])
        l_names.add(r[i['loser_name']])


###################################################################################

###################################################################################
import pandas as pd
# i giocatori con mano U e altre mani sono solo i losers.

tennisDf_pd = pd.read_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\tennis.csv")
# salvo i giocatori con le relative mani
players_hands = tennisDf_pd.drop_duplicates(subset=['loser_id', 'loser_name','loser_hand'])

# conto quante mani usano i giocatori
count_hands = players_hands.groupby(['loser_name'])['loser_name'].count()
# filtro manentendo solo i giocatori che usano più di una mano
players_w2hands = count_hands[count_hands > 1]

# salvo nome giocatore come chiave e come valori le mani che questo usa
player_2hands = {}

for player_name, _ in players_w2hands.items():
    # individuo le mani uniche che usa il giocatore. Se il giocatore usa U e poi U questo non verrà 
    # visualizzato nel risultato
    hands = tennisDf_pd[tennisDf_pd['loser_name']==player_name]['loser_hand'].unique() 
    # se le mani diverse che usa sono più di una:
    if len(hands) > 1:
        player_2hands[player_name] = list(hands)
# rimuovo tutte le mani U in modo tale da mantere le mani reali      
for player_name, hands in player_2hands.items():
    try:
        player_2hands[player_name].remove('U') 
    except:
        continue

# questo giocatore ha come mani 'nan' e 'U' quindi lo rimuoviamo manualmente
del player_2hands['Giuseppe Tresca']

##########################################################################################
# CREO DIZIONARIO PLAYERS_FINAL NEL QUALE SALVO LE RIGHE DA SCRIVERE SUL FILE DI OUTPUT  #
##########################################################################################

visited_w = set()
visited_l = set()
players_final = dict()
#players_final structure:
# idx, val: 0 name, 1 sex, 2 hand, 3 ht, 4 ioc, 5 byear_of_birth    
# index, col: 0 data, 1 name, 2 id, 3 hand, 4 ht, 5 country_id, 6 age

for row in winners: # per ogni riga di winners
    # se il player_id non è stato visitato in winners
    if row[2] not in visited_w: 
        # lo aggiungo ai visitati winners
        visited_w.add(row[2])
        # aggiungo player_id come chiave al dizionario che verrà usato per scrivere
        players_final[row[2]]=[]
        
        """ NAME """
        # aggiungo il nome
        players_final[row[2]].append(row[1])  
        
        """SEX"""
        # se il player è male/female_players aggiungo il sex altrimenti aggiungo NAN
        try:
            players_final[row[2]].append(players[row[1]]) 
        except:
            players_final[row[2]].append('')
       
        """ HAND """   
        # se la mano è U (undefined)
        if row[3] == 'U':
            # se il giocatore ha usato altre mani in altri match e quindi sta in player_2hands
            if row[1] in player_2hands.keys():
                # aggiungi la mano corretta
                players_final[row[2]].append(player_2hands[row[1]][0])
            else:
                # altrimenti la U equivale ad un NAN
                players_final[row[2]].append('') 
        else:
            # se il giocatore ha mano diversa da U aggiungi la mano.
            players_final[row[2]].append(row[3]) 
            
        """ HT """       
        players_final[row[2]].append(row[4]) 
        
        """ COUNTRY_ID """
        players_final[row[2]].append(row[5]) 
        
        """ B_YEAR_OF_BIRTH """
        # se age non è nulla
        if row[6] != '': 
            # calcolo l'anno di nascita
            byear_of_birth = int(row[0][:4]) - int(float(row[6]))
            # aggiungo l'anno di nascita
            players_final[row[2]].append(byear_of_birth) 
        else:
            # altrimenti se age è nullo, l'anno di nascita sarà NULL
            players_final[row[2]].append('')
                 
for row in losers:
    # se il player_id non è stato visitato nei losers e non è stato visitano nei winners
    if row[2] not in visited_l and row[2] not in visited_w:
        # aggiungo player_id ai visitati losers
        visited_l.add(row[2])
        # aggiungo player_id come chiave al dizionario che verrà usato per scrivere
        players_final[row[2]]=[]
        
        """ NAME """
        #aggiungo il nome
        players_final[row[2]].append(row[1])  
        
        """ SEX """
        # se il player è male/female_players aggiungo il sex altrimenti aggiungo NAN
        try:
            players_final[row[2]].append(players[row[1]])
        except:
            players_final[row[2]].append('') #sex
        
        """ HAND """  
        # se la mano è Undefined (U)
        if row[3] == 'U':
            # se il giocatore ha usato altre mani in altri match e quindi sta in player_2hands
            if row[1] in player_2hands.keys():
                # aggiungi la mano corretta
                players_final[row[2]].append(player_2hands[row[1]][0])
            else:
                # altrimenti la U equivale ad un NAN
                players_final[row[2]].append('') 
        else:
            # se il giocatore ha mano diversa da U aggiungi la mano.
            players_final[row[2]].append(row[3]) 
        
        """ HT """
        players_final[row[2]].append(row[4]) 
        
        """ COUNTRY_ID """
        # abbiamo notato che tra i losers c'è un player che ha come country_id ITF al posto di ITA
        # modifico manualmente
        if row[5] == 'ITF':
            players_final[row[2]].append('ITA') 
        else:       
            players_final[row[2]].append(row[5]) 
        
        """ B_YEAR_OF_BIRTH """
        # se age non è nulla
        if row[6] != '': 
            # calcolo l'anno di nascita
            byear_of_birth = int(row[0][:4]) - int(float(row[6]))
            # aggiungo l'anno di nascita
            players_final[row[2]].append(byear_of_birth)
        else:
            # se age è nulla allora l'anno di nascita sarà NULL
            players_final[row[2]].append('')


#######################################
#  WRITE OUTPUT FILE - PLAYERS.CSV    #
#######################################

# aggiusto il sesso dei giocatori presenti in tennis ma non in male_players e female_players
# NOTA: tutti i giocatori presenti in tennis ma non in male_players e female_players sono M ad eccezione
# di Alona Fomina che è F. 

players2fix = (w_names & l_names) - set(players.keys())
#print(players2fix)
#print(len(players2fix))

count = 0
header = 'player_id'+','+'name'+','+'sex'+','+'hand'+','+'ht'+',' + \
    'country_id'+',' + 'byear_of_birth' + '\n'

with open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\players.csv", "w") as players_csv:
    players_csv.write(header)
   
    for player_id, values in players_final.items():
        count +=1
        # scrivo il player_id che corrisponde alla chiave di players_final
        line2write = str(player_id) + ','
    
        for i in range(len(values)):
            if i == 1:
                # se il nome del player è in players2fix
                # significa che bisogna aggiustare il sesso di quei giocatori 
                # presenti in players ma non in male/female_players
                if values[0] in players2fix:
                    # se il nome è Alona Fomina (è l'unica donna di players2fix)
                    if values[0] == 'Alona Fomina':
                        # scrivo F
                        line2write += 'F' + ','
                    else:
                        # i restanti sono M
                        line2write += 'M' +',' 
                else:
                    # se il nome del player non è in players2fix allora inserisco normalemente 
                    # i suoi valori
                    line2write += str(values[i] +',')          
            # se è l'ultimo attibuto
            elif i == len(values)-1:
                line2write += str(values[i]) +'\n'          
            else:      
                line2write += str(values[i]) +','
            
        players_csv.write(line2write)
        
        # Abbiamo notato che un player risulta essere alto 2 cm. 
        # questa altezza è stata considerata come un NUll e successivamente 
        # sostituita con l'altezza media
        
