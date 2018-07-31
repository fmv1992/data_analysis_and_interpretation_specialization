"""
Created on Tue May 17 07:49:53 2016

Author: Felipe M. Vieira

Description: Logistic regression model

Explanatory variables:
GDP per capita (constant 2005 US$)
    NY.GDP.PCAP.KD
Women who believe a husband is justified in beating his wife (any of five reasons) (%)
    SG.VAW.REAS.ZS
Women who were first married by age 18 (% of women ages 20-24)
    SP.M18.2024.FE.ZS
Firms with female top manager (% of firms)
    IC.FRM.FEMM.ZS
Female legislators, senior officials and managers (% of total)
    SG.GEN.LSOM.ZS
Female headed households (% of households with a female head)
    SP.HOU.FEMA.ZS
Proportion of seats held by women in national parliaments (%)
    SG.GEN.PARL.ZS

Response variable:
Law mandates nondiscrimination based on gender in hiring (1=yes; 0=no)
    SG.LAW.NODC.HR
"""
import pandas as pd  # version '0.17.0'
import seaborn  # version '0.7.0'
import matplotlib.pyplot as plt  # version'1.3.1'
import scipy  # version 0.16.1
import numpy as np  # version 1.10.4
import pandas_utilities  # for cosmetic adjustments and data standardization
import statsmodels.api as sm
import statsmodels.formula.api as smf  # version 0.6.1

# data reading, selecting and managing
db = pd.read_csv(
    'world_bank_selected_non_discriminating_based_on_gender_indicators.csv')

db['latest_indicator'] = pd.to_numeric(db['latest_indicator'], errors='coerce')

print('Data management:')
# data renaming to meaningful names
d = {'SG.GEN.PARL.ZS': 'propr_seats_woman_parliaments',
     'NY.GDP.PCAP.KD': 'gdp_per_capita',
     'SG.VAW.REAS.ZS': 'believes_beating_by_hus_justified',
     'SP.M18.2024.FE.ZS': 'fem_first_married_by_18',
     'IC.FRM.FEMM.ZS': 'firms_with_fem_top_manag',
     'SG.GEN.LSOM.ZS': 'fem_leg_senoff_manag',
     # variable is not available...
     'SG.LAW.NODC.HR': 'law_mandates_non_discr',
     'SP.HOU.FEMA.ZS': 'fem_headed_households'}

db['series_code'] = db['series_code'].map(d)

# rearranging data and excluding bogus variables
ct = db.pivot(
    index='series_code',
    columns='country_code',
    values='latest_indicator')
print('A lot of good variables should be excluded because there is not'
      'enough data on them:\n(number of missing countries for each variable)')
print(ct.isnull().sum(axis=1).sort_values(ascending=False))

print('\nDropping bogus variables (too few entries):')
# drops empty variables in the data set until there are at least 60 countries
for empty_variable in ct.isnull().sum(
        axis=1).sort_values(
        ascending=False).index:
    if len(ct.dropna(axis=1).columns) > 60:
        ct.dropna(axis=1, inplace=True)
        break
    else:
        print('Dropping variable {0}'.format(empty_variable))
        ct.drop(empty_variable, inplace=True)

print('\nCentering the quantitative variables:')
# centering the quantitative variables
for quantitative in ['fem_leg_senoff_manag', 'firms_with_fem_top_manag',
                     'gdp_per_capita', 'propr_seats_woman_parliaments']:
    print('Centering variable {0}: mean before: {1:2.2f}'.format(
        quantitative, ct.loc[quantitative, :].mean(axis=0)))
    ct.loc[quantitative, :] -= ct.loc[quantitative, :].mean(axis=0)
    print('After centering: {0:2.2e}'.format(
        ct.loc[quantitative, :].mean(axis=0)))

# logistic regression:
print(
    '\nThe variables left in the model (see code above for the rationale) are:\n{0} where \'law_mandates_non_discr\' is the response variable.'.format(
        '\n'.join(
            list(
                ct.index))))

# first with only one variable: fem_leg_senoff_manag
lreg1 = smf.logit(
    formula='law_mandates_non_discr ~ fem_leg_senoff_manag',
    data=ct.T).fit()
print('Investigating confounding: one variable')
print(lreg1.summary())

# first with only two variables: fem_leg_senoff_manag
lreg1 = smf.logit(
    formula='law_mandates_non_discr ~ fem_leg_senoff_manag + firms_with_fem_top_manag',
    data=ct.T).fit()
print('Investigating confounding: two variables')
print(lreg1.summary())

# full with all variables
lreg1 = smf.logit(
    formula='law_mandates_non_discr ~ fem_leg_senoff_manag + firms_with_fem_top_manag + gdp_per_capita',
    data=ct.T).fit()
print('Full report (all variables)')
print(lreg1.summary())
# odds ratios
print("Odds Ratios")
print(np.exp(lreg1.params))
