"""
Created on Sat May 14 12:24:08 2016

Author: Felipe M. Vieira

Description:

Cuts the database to contain only the following variables:

"""
import numpy as np
import pandas as pd  # version '0.17.0'
import pandas_utilities  # for cosmetic adjustments and data standardization

db = pd.read_csv(
    'wdi_data_all_time_utf8_encoded_and_compressed.csv.gz',
    index_col=0)

pandas_utilities.clean_dataframe(db)
db.rename(columns={'indicator_code': 'series_code'}, inplace=True)

variables_considered = ['NY.GDP.PCAP.KD',
                        'SG.VAW.REAS.ZS',
                        'SP.M18.2024.FE.ZS',
                        'IC.FRM.FEMM.ZS',
                        'SG.GEN.LSOM.ZS',
                        'SP.HOU.FEMA.ZS',
                        'SG.GEN.PARL.ZS',
                        'SG.LAW.NODC.HR'
                        ]

db = db[db.series_code.isin(variables_considered)]
db['latest_indicator'] = np.nan

for year in reversed(range(2006, 2016)):
    db.loc[db['latest_indicator'].isnull(),
           'latest_indicator'] = db.loc[db['latest_indicator'].isnull(),
                                        str(year)]
    print('total data points after adding year {0}: {1}'.format(
        year, db['latest_indicator'].notnull().sum()))

db['latest_indicator'] = pd.to_numeric(db['latest_indicator'], errors='coerce')

db.index.name = 'index'
db.to_csv(
    'world_bank_selected_non_discriminating_based_on_gender_indicators.csv',
    columns=[
        'country_code',
        'series_code',
        'latest_indicator'])
