# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 17:54:35 2016

Author: Felipe M. Vieira
"""
import pandas as pd  # version '0.18.0'
import seaborn  # version '0.7.0'
import matplotlib.pyplot as plt  # version'1.3.1'

db = pd.read_csv('01_u.s._national_epidemiological_survey_on_alcohol_and'
                 '_related_conditions_nesarc.csv', low_memory=False)
db.rename(columns=lambda x: str(x).lower(), inplace=True)
db[['chld0', 'chld1_4', 'chld5_12', 'numpers', 's1q1g']].to_csv(
'03_assignment_nesarc_subset.csv')