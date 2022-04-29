# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 16:01:56 2021

@author: Gaetano Antonicchio, Gloria Segurini
Geography.csv

"""
lang_in = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\country_list.csv", "r")
countries = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\countries.csv", "r")
geography = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\geography.csv", "w")

# Dizionario in cui salvo la nazione come chiave e la lingua come valore
# generato partendo da country_list.csv
coun_lang = dict()

first = True
for row in lang_in:
    if first:  # skip header
        first = False
        continue
    r = row.strip().split(',')
    # Queste nazioni necessitavano di una modifica manuale in quanto
    # era necessario far combaciare i nomi delle chiavi tra il file country_list e countries
    # inoltre alcune lingue erano segnate incorrettamente, quindi sono state modificate.

    if r[1] == 'United Kingdom':
        coun_lang['Great Britain'] = 'English'
    elif r[1] == 'United States':
        coun_lang['United States of America'] = r[4]
    elif r[1] == 'Rí©union':
        coun_lang['Reunion'] = 'French'
    elif r[1] == 'Russia':
        coun_lang[r[1]] = 'Russian'
    elif r[1] == 'Cuba':
        coun_lang[r[1]] = 'Spanish'
    elif r[1] == 'Barbados':
        coun_lang[r[1]] = 'English'
    elif r[1] == 'Grenada':
        coun_lang[r[1]] = 'English'
    elif r[1] == 'Bahamas':
        coun_lang[r[1]] = 'English'
    elif r[1] == 'Namibia':
        coun_lang[r[1]] = 'English'
    elif r[1] == 'Guam':
        coun_lang[r[1]] = 'English'
    elif r[1] == 'Gabon':
        coun_lang[r[1]] = 'French'
    elif r[1] == 'Guadeloupe':
        coun_lang[r[1]] = 'French'
    elif r[1] == 'Cameroon':
        coun_lang[r[1]] = 'French'
    elif r[1] == 'Madagascar':
        coun_lang[r[1]] = 'French'
    elif r[1] == 'Moldova':
        coun_lang[r[1]] = 'Romanian'
    elif r[1] == 'Cyprus':
        coun_lang[r[1]] = 'Greek'
    elif r[1] == 'Samoa':
        coun_lang[r[1]] = 'Samoan'
    elif r[1] == 'Mauritius':
        coun_lang[r[1]] = 'Mauritian Creole'
    elif r[1] == 'Burundi':
        coun_lang[r[1]] = 'Kirundi'
    elif r[1] == 'Haiti':
        coun_lang[r[1]] = 'Spanish'
    elif r[1] == 'Andorra':
        coun_lang[r[1]] = 'Catalan'
    elif r[1] == 'Canada':
        coun_lang[r[1]] = 'English'
    elif r[1] == 'France':
        coun_lang[r[1]] = 'French'
    elif r[1] == 'Macedonia':
        coun_lang['North Macedonia'] = r[4]
    elif r[1] == 'Germany':
        coun_lang['Germany'] = 'German'
    elif r[1] == 'Netherlands':
        coun_lang['Netherlands'] = 'Dutch'

    else:
        coun_lang[r[1]] = r[4]
# aggiungo il Kosovo che non era presente in country_list
coun_lang['Kosovo'] = 'Serbian'

###############################################################################
#                        SCRIVO GEOGRAPHY.CSV                                 #
###############################################################################

# Scrivo l'header del file geography.csv
geography.writelines('country_id'+',' + 'language'+','+'continent'+'\n')

# Scrivo le righe del file geography.csv
# NOTA: Alcune nazioni presentavano degli errori sintattici in countries, queste sono state
# modificate manualmente

first = True
visited = set()  # usata per eliminare righe duplicate

for row in countries:
    token = row.strip().split(',')
    if first: # Skip Header
        first = False 
    else:
        # se il country_id non è in visited
        if token[0] not in visited: 
            # lo aggiungo
            visited.add(token[0])
            
            if token[1] == 'Urugay':
                string2write = str(token[0]+','+coun_lang['Uruguay']+',' + token[2]+'\n')
                geography.writelines(string2write)
            
            elif token[1] == 'New Zeland':
                string2write = str(token[0] + ','+'English'+',' + token[2]+'\n')
                geography.writelines(string2write)

            elif token[0] == 'POC':
                string2write = str('POC'+','+'Malesian'+','+'Oceania'+'\n')
                geography.writelines(string2write)

            elif token[0] == 'ITF': 
                string2write = str('ITA', +','+'Italian'+','+'Europe' + '\n')
                geography.writelines(string2write)
            
            # se il nome della nazione è nel dizionario in cui abbiamo associato la lingua
            elif token[1] in coun_lang.keys():
                # LEGEND:
                # token[0] = country_ioc, token[1] = country_name, coun_lang[token[1]] = language
                
                #prendi quella lingua e scrivi la riga
                string2write = str(token[0] + ',' + coun_lang[token[1]]+',' + token[2]+'\n')
                geography.writelines(string2write)
            else:
                # altrimenti la lingua sarà NAN
                string2write = str(token[0] + ',' + '' + ','+token[2]+'\n')
                geography.writelines(string2write)

geography.close()
##################################################################################
#  CONTROLLO SE CI SONO COUNTRY_ID IN PLAYERS CHE SONO ASSENTI DA GEOGRAPHY.CSV  #
##################################################################################

players = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\players.csv", "r")
geo_r = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\geography.csv", "r")

# set che servono per individuare i country_id mancanti da geography
pl_countryid = set()
geo_countryid = set()

### COSTRUISCO pl_country_id
first = True
for line in players.readlines():
    if first: #Skip Header
        first = False
    token = line.strip().split(',')
    # se il country_id di players non è in pl_countryid:
    #if token[5] not in pl_countryid:
        
    # aggiungo il country_id da players    
    pl_countryid.add(token[5])

# COSTRUISCO geo_countryid
first = True
for line in geo_r.readlines():
    if first:
        first = False
    token = line.strip().split(',')
    #if token[0] not in geo_countryid:  # if the country_ioc not in pl_countryioc
    # aggiungo il country_id da geography
    geo_countryid.add(token[0])

# Determino country_id mancanti
missing_ioc = pl_countryid - geo_countryid
#print('missing_ioc :', missing_ioc)  #decommenta per stampare nazioni mancanti

geo_r.close()
players.close()

# Scrivo le nazioni mancanti su geography.csv
# le infomazioni sono state recuperate manualmente consultando Wikipedia

with open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\geography.csv", "a") as geo_w:
    for ioc in missing_ioc:
        if ioc == 'BEN':
            geo_w.writelines('BEN' + ',' + 'French'+','+'Africa'+'\n')
        elif ioc == 'MRN':
            geo_w.writelines('MRN'+','+'French'+','+'America'+'\n')
        elif ioc == 'LVA':
            geo_w.writelines('LVA'+','+'Latvian'+','+'Europe'+'\n')
        elif ioc == 'ANT':
            geo_w.writelines('ANT'+','+'English'+','+'America'+'\n')
        elif ioc == 'BAN':
            geo_w.writelines('BAN'+','+'Bengali'+','+'Asia'+'\n')
        elif ioc == 'TOG':
            geo_w.writelines('TOG'+','+'French'+','+'Africa'+'\n')
        elif ioc == 'LBN':
            geo_w.writelines('LBN'+','+'Arabic'+','+'Asia' + '\n')
        elif ioc == 'SAU':
            geo_w.writelines('SAU'+','+'Arabic'+','+'Asia'+'\n')
        elif ioc == 'TKM':
            geo_w.writelines('TKM'+','+'Turkmen'+','+'Asia'+'\n')
        elif ioc == 'COD':
            geo_w.writelines('COD'+','+'French'+','+'Africa'+'\n')
        elif ioc == 'GHA':
            geo_w.writelines('GHA'+','+'English'+','+'Africa'+'\n')
        elif ioc == 'AZE':
            geo_w.writelines('AZE'+','+'Azerbaijani'+','+'Asia'+'\n')
        elif ioc == 'TTO':
            geo_w.writelines('TTO'+','+'English'+','+'America'+'\n')
        elif ioc == 'SMR':
            geo_w.writelines('SMR'+','+'Italian'+','+'Europe'+'\n')
        elif ioc == 'AHO':
            geo_w.writelines('AHO'+','+'Dutch'+','+'America'+'\n')
        elif ioc == 'VIN':
            geo_w.writelines('VIN'+','+'English'+','+'America'+'\n')
        elif ioc == 'QAT':
            geo_w.writelines('QAT'+','+'Arabic'+','+'Asia'+'\n')
        elif ioc == 'BER':
            geo_w.writelines('BER'+','+'English'+','+'America'+'\n')
        elif ioc == 'SYR':
            geo_w.writelines('SYR'+','+'Arabic'+','+'Asia'+'\n')
        elif ioc == 'BOT':
            geo_w.writelines('BOT'+','+'English'+','+'Africa'+'\n')
        elif ioc == 'BRN':
            geo_w.writelines('BRN'+','+'Malay'+','+'Asia'+'\n')
        elif ioc == 'JOR':
            geo_w.writelines('JOR'+','+'Arabic'+','+'Asia'+'\n')
        elif ioc == 'ZAM':
            geo_w.writelines('ZAM'+','+'English'+','+'Africa'+'\n')
        elif ioc == 'LBA':
            geo_w.writelines('LBA'+','+'Arabic'+','+'Africa'+'\n')
        elif ioc == 'CRI':
            geo_w.writelines('CRI'+','+'Spanish'+','+'America'+'\n')
        elif ioc == 'ERI':
            geo_w.writelines('ERI'+','+'Tigryna'+','+'Africa'+'\n')
        elif ioc == 'JAM':
            geo_w.writelines('JAM'+','+'English'+','+'America'+'\n')
        elif ioc == 'UAE':
            geo_w.writelines('UAE'+','+'Arabic'+','+'Asia'+'\n')
        else:
            geo_w.writelines('BGR'+','+'Bulgarian'+','+'Europe'+'\n')
