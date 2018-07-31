"""
Subset NESARC data.

This script has been commented out because the subset data is available, but
not the original one.

Author: Felipe M. Vieira
"""

import os

import pandas as pd  # version '0.18.0'
import seaborn  # version '0.7.0'
import matplotlib.pyplot as plt  # version'1.3.1'

from project_library import DATASETS_PATH

# db = pd.read_csv(os.path.join(DATASETS_PATH, '01_u.s._national_epidemiological_survey_on_alcohol_and')
#                  '_related_conditions_nesarc.csv', low_memory=False)
# db.rename(columns=lambda x: str(x).lower(), inplace=True)
# db[['chld0', 'chld1_4', 'chld5_12', 'numpers', 's1q1g']].to_csv(
# '03_assignment_nesarc_subset.csv')
