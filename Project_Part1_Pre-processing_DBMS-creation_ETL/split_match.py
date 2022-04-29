# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 17:18:56 2021

@author: Gaetano
"""

# SPLIT MATCH.csv for loading to DB
import pandas as pd

filename = r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\match.csv"

match = pd.read_csv(filename)

col = ['winner_rank', 'winner_rank_points', 'loser_rank', 'loser_rank_points']
for c in col:
    match[c] = match[c].fillna(-1).astype(int)
match.to_csv(filename, sep=',', header=True, index=False)

row_count = 3000
for num, chunk in enumerate(pd.read_csv(filename, chunksize=row_count)): 
    chunk.to_csv(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\split_match\match" + str(num) + ".csv", sep=',', header=True, index=False)