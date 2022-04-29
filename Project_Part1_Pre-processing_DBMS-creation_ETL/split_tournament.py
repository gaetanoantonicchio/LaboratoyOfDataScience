# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 17:26:21 2021

@author: Gaetano
"""

# SPLIT TOURNAMENT.csv for loading to DB

import pandas as pd

filename = r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\tournament.csv"
row_count = 2000
for num, chunk in enumerate(pd.read_csv(filename, chunksize=row_count)): 
    chunk.to_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\split_tournament\tournament" + str(num) + ".csv")