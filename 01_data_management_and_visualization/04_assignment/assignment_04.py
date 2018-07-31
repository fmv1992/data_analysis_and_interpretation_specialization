"""
Created on Sun Apr 17 14:00:51 2016

Author: Felipe M. Vieira

Description:

Assignment 04

"""

import os


import pandas as pd  # version '0.18.0'
import seaborn  # version '0.7.0'
import matplotlib.pyplot as plt  # version'1.3.1'
import numpy as np

from project_library import DATASETS_PATH

# importing and cleaning of the database
gapminder = pd.read_csv(os.path.join(DATASETS_PATH, '04_gapminder.csv'), index_col='country')
gapminder.rename(index=lambda x: str(x).lower(), inplace=True)
gapminder.dropna(inplace=True)

#gapminder = gapminder.applymap(lambda x: np.nan if x == ' ' else x)
gapminder = gapminder.apply(pd.to_numeric, args=('coerce',))

# univariate analysis of polity score
plt.figure(0)
plt.hist(gapminder.polityscore.dropna(), bins=np.arange(-10.5, 11, 0.5),
         normed=True)
plt.xticks(range(-10, 11, 1))
plt.xlabel('Polity Score')
plt.ylabel('Normalized Frequency')
plt.tight_layout()
plt.savefig('univariate_polity_score.png', dpi=500)
plt.show()
plt.close(0)
print('Univariate analysis: polity score:\nMean: \t{0:2.2f}\nMedian: '
      '\t{1:2.2f}\nMode: \t{2:2.2f}\nStandard Deviation: \t{3:2.2f}'.format(
          gapminder.polityscore.dropna().mean(),
          gapminder.polityscore.dropna().median(),
          gapminder.polityscore.dropna().mode()[0],
          gapminder.polityscore.dropna().std()
      ))

# bivariate analysis of co2emissions and incomeperperson
plt.figure(1)
plt.scatter(gapminder.dropna().incomeperperson,
            gapminder.dropna().co2emissions)
plt.xlabel('Income per Person')
plt.ylabel('CO2 emissions')
plt.tight_layout()
plt.savefig('bivariate_income_versus_co2emissions.png', dpi=500)
plt.show()
plt.close(1)
