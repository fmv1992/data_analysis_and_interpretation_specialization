# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 17:54:35 2016

@author: e061568
"""
import pandas as pd  # version '0.18.0'
import seaborn  # version '0.7.0'
import matplotlib.pyplot as plt  # version'1.3.1'
import numpy as np

# reads the input file
db = pd.read_csv('03_assignment_nesarc_subset.csv',
                 index_col=0, low_memory=False)

# renames some columns to meaningful names
db.rename(columns={'numpers':'n_persons',
                   's1q1g':'years_in_us'}, inplace=True)

# converts years in us to int 
db.years_in_us = pd.to_numeric(db.years_in_us, errors='coerce')
db['n_children'] = db['chld0'] + db['chld1_4'] + db['chld5_12']

# aggregates years in us into 5 years range since there is a 100 long range
# of values
group_y_in_us = pd.groupby(db, by='years_in_us')

# prints 
for c in ['n_children', 'years_in_us', 'n_persons']:
    print(c, db[c].value_counts(normalize=True), sep='\n')