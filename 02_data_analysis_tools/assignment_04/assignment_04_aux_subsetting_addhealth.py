# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 08:17:14 2016

Author: Felipe Vieira
"""
import pandas as pd  # version '0.18.0'

# creates a map from meaningless names to meaningful ones
col_map = {
    'H1ED11': 'grade_language_arts',
    'H1ED13': 'grade_history_social_studies',

    'H1ED12': 'grade_math',
    'H1ED14': 'grade_science',

    'H1ED22': 'happy_at_school'
}

# imports the data set and manages it
db_subset = pd.read_csv('03_national_longitudinal_study_of_adolescent_health_'
                        'addhealth.csv', usecols=col_map.keys())
db_subset.index.name = 'id'
db_subset.rename(columns=col_map, inplace=True)

db_subset.to_csv('03_national_longitudinal_study_of_adolescent_health_'
                 'addhealth_subset.csv', col_map=col_map.values())
