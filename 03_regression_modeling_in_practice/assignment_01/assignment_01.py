"""
Created on Tue Apr 26 07:59:05 2016

Author: Felipe M. Vieira

Description:

Assignment 01 for Regression Modelling in Practice

"""

import os

import pandas as pd  # version '0.17.0'
import seaborn  # version '0.7.0'
import matplotlib.pyplot as plt  # version'1.3.1'
import scipy  # version 0.16.1
import pandas_utilities  # for cosmetic adjustments and data standardization

from project_library import DATASETS_PATH

db = pd.read_csv(os.path.join(DATASETS_PATH, 'world_bank_all_indicators_2010.csv'))
db = db.rename(columns=lambda x: x.lower().replace(' ', '_'))

unique_countries = db['country_name'].unique()[:-1]

print('List of countries:')
for i in unique_countries:  # drops last since it is 'nan'
    print(i)
print('\nTotal of {} countries'.format(len(unique_countries)))

infra_db = pd.read_csv(os.path.join(DATASETS_PATH, 'world_bank_infrastructure_indicators_codebook.csv'))
pandas_utilities.clean_dataframe(infra_db)

print('\n\nList of variables in the \'Infrastructure\' subset:')
for code, name in zip(infra_db['indicator_name'], infra_db['indicator_code']):
    print(code, '[', name, ']')

energetic_matrix = {
    'EG.ELC.COAL.ZS': 'coal',
    'EG.ELC.HYRO.ZS': 'hydroeletric',
    'EG.ELC.NGAS.ZS': 'natural_gas',
    'EG.ELC.NUCL.ZS': 'nuclear',
    'EG.ELC.PETR.ZS': 'oil_sources',
}
plot_dict = {}
for key, value in energetic_matrix.items():
    plot_dict[value] = float(
        db.loc
        [(db.country_name == 'Brazil') & (db.series_code == key),
         '2010_[yr2010]'])
plt.bar(range(len(plot_dict)), list(plot_dict.values()), align='center')
plt.xticks(range(len(plot_dict)), list(plot_dict.keys()))
plt.title('Electric Energy Sources for Brazil')
plt.ylabel('Share (%)')
plt.tight_layout()
plt.savefig('electric_energy_sources_brazil.png', dpi=500)
plt.show()
