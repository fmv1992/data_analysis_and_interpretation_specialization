# -*- coding: utf-8 -*-
"""
Created on Sat May 14 12:24:08 2016

Author: Felipe M. Vieira

Description:

Cuts the database to contain only the following variables:

AG.LND.AGRI.ZS	Agricultural land (% of land area)	Agricultural land refers to the share of land area that is arable, under permanent crops, and under permanent pastures. Arable land includes land defined by the FAO as land under temporary crops (double-cropped areas are counted once), temporary meadows for mowing or for pasture, land under market or kitchen gardens, and land temporarily fallow. Land abandoned as a result of shifting cultivation is excluded. Land under permanent crops is land cultivated with crops that occupy the land for long periods and need not be replanted after each harvest, such as cocoa, coffee, and rubber. This category includes land under flowering shrubs, fruit trees, nut trees, and vines, but excludes land under trees grown for wood or timber. Permanent pasture is land used for five or more years for forage, including natural and cultivated crops.	Food and Agriculture Organization, electronic files and web site.

AG.LND.TRAC.ZS	Agricultural machinery, tractors per 100 sq. km of arable land	Agricultural machinery refers to the number of wheel and crawler tractors (excluding garden tractors) in use in agriculture at the end of the calendar year specified or during the first quarter of the following year. Arable land includes land defined by the FAO as land under temporary crops (double-cropped areas are counted once), temporary meadows for mowing or for pasture, land under market or kitchen gardens, and land temporarily fallow. Land abandoned as a result of shifting cultivation is excluded.	Food and Agriculture Organization, electronic files and web site.
    replaced by
AG.LND.PRCP.MM	Average precipitation in depth (mm per year)	Average precipitation is the long-term average in depth (over space and time) of annual precipitation in the country. Precipitation is defined as any kind of water that falls from clouds as a liquid or a solid.	Food and Agriculture Organization, electronic files and web site.
    replaced by
AG.LND.ARBL.ZS	Arable land (% of land area)	Arable land includes land defined by the FAO as land under temporary crops (double-cropped areas are counted once), temporary meadows for mowing or for pasture, land under market or kitchen gardens, and land temporarily fallow. Land abandoned as a result of shifting cultivation is excluded.	Food and Agriculture Organization, electronic files and web site.

AG.CON.FERT.ZS	Fertilizer consumption (kilograms per hectare of arable land)	Fertilizer consumption measures the quantity of plant nutrients used per unit of arable land. Fertilizer products cover nitrogenous, potash, and phosphate fertilizers (including ground rock phosphate). Traditional nutrients--animal and plant manures--are not included. For the purpose of data dissemination, FAO has adopted the concept of a calendar year (January to December). Some countries compile fertilizer data on a calendar year basis, while others are on a split-year basis. Arable land includes land defined by the FAO as land under temporary crops (double-cropped areas are counted once), temporary meadows for mowing or for pasture, land under market or kitchen gardens, and land temporarily fallow. Land abandoned as a result of shifting cultivation is excluded.	Food and Agriculture Organization, electronic files and web site.

EA.PRD.AGRI.KD	Agriculture value added per worker (constant 2005 US$)	Agriculture value added per worker is a measure of agricultural productivity. Value added in agriculture measures the output of the agricultural sector (ISIC divisions 1-5) less the value of intermediate inputs. Agriculture comprises value added from forestry, hunting, and fishing as well as cultivation of crops and livestock production. Data are in constant 2005 U.S. dollars.	Derived from World Bank national accounts files and Food and Agriculture Organization, Production Yearbook and data files.
"""
import pandas as pd  # version '0.17.0'
import seaborn  # version '0.7.0'
import matplotlib.pyplot as plt  # version'1.3.1'
import scipy  # version 0.16.1
import numpy as np  # version 1.10.4
import pandas_utilities  # for cosmetic adjustments and data standardization
import statsmodels.api as sm
import statsmodels.formula.api as smf  # version 0.6.1

# loading the database
db = pd.read_csv('world_bank_selected_agricultural_indicators.csv')
db.drop(['series_name', 'index'], axis=1, inplace=True)

# renaming variables into meaningful names
rename_vars_dict = {'AG.LND.AGRI.ZS': 'agr_land',
'AG.LND.TRAC.ZS': 'agr_machinery',
'AG.CON.FERT.ZS': 'fert_cons',
'EA.PRD.AGRI.KD': 'agr_value_added',
'AG.LND.PRCP.MM': 'precipitation_mm',
'AG.LND.ARBL.ZS': 'arable_land',
'AG.LND.AGRI.K2': 'agricultural_land'
}
db.series_code = db.series_code.map(rename_vars_dict)
db['2010'] = pd.to_numeric(db['2010'], errors='coerce')

# rearranging data and excluding bogus variables
ct = db.pivot(index='series_code', columns='country_code', values='2010')
# drops empty variables in the data set
ct.drop(['precipitation_mm', 'agr_machinery'], inplace=True)
# only takes into account countries with all the 4 variables
ct.dropna(axis=1, inplace=True)

# centering all explanatory variables
# Agricultural land (% of land area)
print('Mean before centering for agr_land: {0:2.2f}'.format(ct.loc['agr_land'].mean()))
ct.loc['agr_land'] -= ct.loc['agr_land'].mean()
print('Mean after centering for agr_land: {0:2.2e}'.format(ct.loc['agr_land'].mean()))
# Fertilizer consumption
print('Mean before centering for fert_cons: {0:2.2f}'.format(ct.loc['fert_cons'].mean()))
ct.loc['fert_cons'] -= ct.loc['fert_cons'].mean()
print('Mean after centering for fert_cons: {0:2.2e}'.format(ct.loc['fert_cons'].mean()))
#
print('Mean before centering for arable_land: {0:2.2f}'.format(ct.loc['arable_land'].mean()))
ct.loc['arable_land'] -= ct.loc['arable_land'].mean()
print('Mean after centering for arable_land: {0:2.2e}'.format(ct.loc['arable_land'].mean()))

# adjusting my response variable
ct.loc['agr_value_added_per_worker_per_land'] = ct.loc['agr_value_added'] / ct.loc['agricultural_land']

# regression
reg1 = smf.ols('agr_value_added_per_worker_per_land ~ agr_land + fert_cons + arable_land', data=ct.T).fit()
print('\n\n',reg1.summary())

# qq plot
plt.figure(1)
fig1 = sm.qqplot(reg1.resid, line='r')
plt.savefig('qq_plot.png', dpi=500)
plt.close()

# standardized residuals for all observations
stdres = pd.DataFrame(reg1.resid_pearson)
plt.figure(2)
plt.plot(stdres, 'o', ls='None')
l = plt.axhline(y=0, color='r')
plt.ylabel('Standardized Residual')
plt.xlabel('Observation Number')
plt.savefig('std_res.png', dpi=500)
plt.close()

# leverage plot
plt.figure(3)
fig3 = sm.graphics.influence_plot(reg1)
plt.savefig('leverage_plot.png', dpi=500)
plt.close()

# checking for confounding between arable land and agricultural land
conf = scipy.stats.pearsonr(ct.loc['arable_land'], ct.loc['agricultural_land'])
print('R value between arable land and agricultural land: {0:2.3f}\np-value: {1:2.3f}'.format(conf[0], conf[1]))