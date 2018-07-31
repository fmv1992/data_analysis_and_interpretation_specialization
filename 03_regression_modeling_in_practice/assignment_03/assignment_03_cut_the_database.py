"""
Created on Sat May 14 12:24:08 2016

Author: Felipe M. Vieira

Description:

Cuts the database to contain only the following variables:

Explanatory variables:
AG.LND.AGRI.ZS	Agricultural land (% of land area)	Agricultural land refers to the share of land area that is arable, under permanent crops, and under permanent pastures. Arable land includes land defined by the FAO as land under temporary crops (double-cropped areas are counted once), temporary meadows for mowing or for pasture, land under market or kitchen gardens, and land temporarily fallow. Land abandoned as a result of shifting cultivation is excluded. Land under permanent crops is land cultivated with crops that occupy the land for long periods and need not be replanted after each harvest, such as cocoa, coffee, and rubber. This category includes land under flowering shrubs, fruit trees, nut trees, and vines, but excludes land under trees grown for wood or timber. Permanent pasture is land used for five or more years for forage, including natural and cultivated crops.	Food and Agriculture Organization, electronic files and web site.
AG.LND.ARBL.ZS	Arable land (% of land area)	Arable land includes land defined by the FAO as land under temporary crops (double-cropped areas are counted once), temporary meadows for mowing or for pasture, land under market or kitchen gardens, and land temporarily fallow. Land abandoned as a result of shifting cultivation is excluded.	Food and Agriculture Organization, electronic files and web site.
AG.CON.FERT.ZS	Fertilizer consumption (kilograms per hectare of arable land)	Fertilizer consumption measures the quantity of plant nutrients used per unit of arable land. Fertilizer products cover nitrogenous, potash, and phosphate fertilizers (including ground rock phosphate). Traditional nutrients--animal and plant manures--are not included. For the purpose of data dissemination, FAO has adopted the concept of a calendar year (January to December). Some countries compile fertilizer data on a calendar year basis, while others are on a split-year basis. Arable land includes land defined by the FAO as land under temporary crops (double-cropped areas are counted once), temporary meadows for mowing or for pasture, land under market or kitchen gardens, and land temporarily fallow. Land abandoned as a result of shifting cultivation is excluded.	Food and Agriculture Organization, electronic files and web site.

Response variables:
EA.PRD.AGRI.KD	Agriculture value added per worker (constant 2005 US$)	Agriculture value added per worker is a measure of agricultural productivity. Value added in agriculture measures the output of the agricultural sector (ISIC divisions 1-5) less the value of intermediate inputs. Agriculture comprises value added from forestry, hunting, and fishing as well as cultivation of crops and livestock production. Data are in constant 2005 U.S. dollars.	Derived from World Bank national accounts files and Food and Agriculture Organization, Production Yearbook and data files.

Auxiliar variables:
AG.LND.AGRI.K2	Agricultural land (sq. km)	Agricultural land refers to the share of land area that is arable, under permanent crops, and under permanent pastures. Arable land includes land defined by the FAO as land under temporary crops (double-cropped areas are counted once), temporary meadows for mowing or for pasture, land under market or kitchen gardens, and land temporarily fallow. Land abandoned as a result of shifting cultivation is excluded. Land under permanent crops is land cultivated with crops that occupy the land for long periods and need not be replanted after each harvest, such as cocoa, coffee, and rubber. This category includes land under flowering shrubs, fruit trees, nut trees, and vines, but excludes land under trees grown for wood or timber. Permanent pasture is land used for five or more years for forage, including natural and cultivated crops.	Food and Agriculture Organization, electronic files and web site.
"""
import pandas as pd  # version '0.17.0'
import pandas_utilities  # for cosmetic adjustments and data standardization

db = pd.read_csv('world_bank_all_indicators_2010.csv')
pandas_utilities.clean_dataframe(db)
db.rename(columns={'2010_yr2010': '2010'}, inplace=True)

variables_considered = ['AG.LND.AGRI.ZS', 'AG.LND.TRAC.ZS', 'AG.CON.FERT.ZS',
                        'EA.PRD.AGRI.KD', 'AG.LND.PRCP.MM', 'AG.LND.ARBL.ZS',
                        'AG.LND.AGRI.K2']

db = db[db.series_code.isin(variables_considered)]
db.index.name = 'index'

db.to_csv('world_bank_selected_agricultural_indicators.csv')
