# -*- coding: utf-8 -*-
'''
Created on Tue May  3 07:24:49 2016

@author: monteiro
'''
import pandas as pd  # version '0.17.0'
import seaborn  # version '0.7.0'
import matplotlib.pyplot as plt  # version'1.3.1'
import scipy  # version 0.16.1
import numpy as np  # version 1.10.4
import pandas_utilities  # for cosmetic adjustments and data standardization
import statsmodels.formula.api as smf  # version 0.6.1

db = pd.read_csv('world_bank_infrastructure_indicators_from_1960_to_2015.csv',
                 engine='python', skiprows = 4)
pandas_utilities.clean_dataframe(db)

# data cleaning
db.drop(['unnamed_60'], axis=1, inplace=True)

# data selection
db = db[['country_code', 'indicator_code', '2012']]
# IQ.WEF.PORT.XQ	Quality of port infrastructure,
#   WEF (1=extremely underdeveloped to 7=well developed and efficient by
#   international standards)
# IS.SHP.GCNW.XQ	Liner shipping connectivity index
#   (maximum value in 2004 = 100)
db = db[(db.indicator_code == 'IS.SHP.GCNW.XQ') |
        (db.indicator_code == 'IQ.WEF.PORT.XQ')]
db.indicator_code = db.indicator_code.map({'IS.SHP.GCNW.XQ':
                                           'liner_connectivity',
                                           'IQ.WEF.PORT.XQ':'port_infra'})
db['port_infra'] = db.where(db.indicator_code == 'port_infra').loc[:, '2012']
db['liner_connectivity'] = db.where(db.indicator_code ==
                                    'liner_connectivity').loc[:, '2012']

db.drop(['indicator_code','2012'], axis=1, inplace=True)

db = pd.pivot_table(db, index=['country_code'])
db.dropna(inplace=True)

# centering the explanatory variable
print('Old mean: {0:2.2f}'.format(db.port_infra.mean()))
db.port_infra = db.port_infra - db.port_infra.mean()
print('New mean: {0:2.2f}'.format(db.port_infra.mean()))

# plotting
plt.figure(1)
scat1 = seaborn.regplot(x='port_infra', y='liner_connectivity',
                        scatter=True, data=db)
plt.xlabel('Quality of port infrastructure')
plt.ylabel('Liner shipping connectivity index')
plt.title ('Scatterplot for the Association Between Quality of port '
           'infrastructure and Liner shipping connectivity index')
plt.tight_layout()
plt.savefig('scatterplot_for_the_association_between_quality_of_port_'
            'infrastructure_and_liner_shipping_connectivity_index', dpi=500)

# producing summary statistics
print ('OLS regression model for the association between quality of port '
       'infrastructure and liner shipping connectivity index')
reg1 = smf.ols('port_infra ~ liner_connectivity', data=db).fit()
print (reg1.summary())
pearson_r = scipy.stats.pearsonr(db.port_infra, db.liner_connectivity)
linregress = scipy.stats.linregress(db.port_infra, db.liner_connectivity)
print('Scipy results for Pearson\'s correlation:')
print('p-value: {0:2.2f}\nr-coefficient:{1:2.2f}'.format(pearson_r[1],
                                                         pearson_r[0]))
print('Regression results:')
print('Slope: {0:2.2f}\nIntercept: {1:2.2f}'.format(linregress.slope,
                                                    linregress.intercept))
print('Formula: liner_connectivity = port_infra * {0:2.2f} + {1:2.2f}'.format(
linregress.slope, linregress.intercept))
#plt.scatter(db.liner_connectivity, db.port_infra)
