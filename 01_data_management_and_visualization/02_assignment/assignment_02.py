"""
Created on Sun Apr  3 21:39:04 2016

Author: Felipe M. Vieira

Description:

Assignment 02
"""

import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from project_library import DATASETS_PATH

# reads data set
df = pd.read_csv(
    os.path.join(
        DATASETS_PATH,
        '04_gapminder.csv'),
    low_memory=False)
# makes names uniform to lowercase
df.country = df.country.apply(str.lower)
# makes all columns numbers
for column in df.columns:
    if column == 'country':
        continue
    df[column] = pd.to_numeric(df[column], errors='coerce')

# so i'm grouping by polityscore (2009 Democracy score (Polity))
subset = df.loc[:, ['incomeperperson', 'armedforcesrate', 'internetuserate',
                    'polityscore']]
g = subset.groupby('polityscore')

# frequency distribution 01: armed forces rate
armed_forces_per_country = g.armedforcesrate.mean()
print('mean armed forces rate per country', armed_forces_per_country)
armed_forces_per_country.plot.bar()
plt.ylabel('Simple average of armed forces rate')
plt.tight_layout()
plt.savefig('armed_forces_rate.png', dpi=300)
plt.show()
plt.close()

# frequency distribution 02: number of countries in each group
countries_per_polity_score = g.size() / g.size().sum()
print('number of countries per polity score:\n', countries_per_polity_score,
      'better shown graphically:')
print('Proportion of countries with polityscores >= 5: {0:1.1%}'.format(
    g.size().loc[5:10].sum() / g.size().sum()))
countries_per_polity_score.plot.bar()
plt.savefig('countries_per_polity_score.png', dpi=300)
plt.show()
plt.close()

# frequency distribution 03: internet rate in the extremes
internet_use_low = g['internetuserate'].get_group(
    -10).sum() / g.size().loc[-10]
internet_use_high = g['internetuserate'].get_group(10).sum() / g.size().loc[10]
print('average internet use rate of high polity score countries:',
      internet_use_high)
print('averate internet use rate of low polity score countries:',
      internet_use_low)
