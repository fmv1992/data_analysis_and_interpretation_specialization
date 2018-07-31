"""
Created on Sun Apr 10 17:54:35 2016

Author: Felipe M. Vieira

Description:

Assignment 03
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
range_of_years = np.arange(0, 101, 10)
db['years_in_us_grouped'] = pd.cut(db.years_in_us, range_of_years,
                                   include_lowest=True)

# prints
for c in ['n_children', 'years_in_us_grouped', 'n_persons']:
    v_counts = db[c].value_counts(normalize=True, sort=False)
    print(c, v_counts, sep='\n')
    v_counts.plot.bar()
    plt.ylabel('frequency of ' + c)
    plt.tight_layout()
    plt.savefig('{0}_plot.png'.format(c), dpi=500)
    plt.show()
    plt.close()
