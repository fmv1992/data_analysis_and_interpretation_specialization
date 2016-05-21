# -*- coding: utf-8 -*-
"""
Created on Sat May 14 12:24:08 2016

Author: monteiro

Description:

Cuts the database to contain only the following variables:

"""
import pandas as pd  # version '0.17.0'
import pandas_utilities  # for cosmetic adjustments and data standardization

db = pd.read_csv('world_bank_all_indicators_2010.csv')
pandas_utilities.clean_dataframe(db)
db.rename(columns={'2010_yr2010': '2010'}, inplace=True)

variables_considered = ['SG.GEN.PARL.ZS', 'NY.GDP.PCAP.KD', 'SG.VAW.REAS.ZS',
                        'SP.M18.2024.FE.ZS', 'IC.FRM.FEMM.ZS', 'SG.GEN.LSOM.ZS',
                        'SG.LAW.NODC.HR', 'SP.HOU.FEMA.ZS']

db = db[db.series_code.isin(variables_considered)]
db.index.name = 'index'

db.to_csv('world_bank_selected_non_discriminating_based_on_gender_indicators.csv')