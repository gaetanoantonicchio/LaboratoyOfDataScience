# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 11:29:43 2021

@author: Gaetano
"""
# Script che esegue un run di tutti i file .py necessari per la creazione
# dei csv

import os
directory = r"C:\Users\Gaetano\Desktop\ProgettoLAB\codici"
os.chdir(directory)  # locate ourselves in the directory
for script in ['splitTennis_match.py', 'splitTennis_date.py',\
               'splitTennis_tournament.py','splitTennis_players.py',\
               'splitTennis_geography.py','post_processing.py']:
    with open(script) as f:
       contents = f.read()
    exec(contents)
    print(script, " executed")
