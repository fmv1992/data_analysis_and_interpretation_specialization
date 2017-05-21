# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 08:45:34 2016

Author: Felipe M. Vieira
"""
import pandas as pd
import numpy as np
import scipy.stats
import seaborn
import matplotlib.pyplot as plt

# loads the data base
mars = pd.read_csv('02_mars_craters_study.csv', usecols=[0, 2, 3])
# rename columns to lower case
mars = mars.rename(columns=dict(zip(mars.columns,
                                    [x.lower() for x in mars.columns]),
                   inplace=True))
# takes a sample to plot and give a hunch on the unvenvess of the distribution
mars_coords = mars[['latitude_circle_image',
                    'longitude_circle_image']].sample(n=2000)
plt.scatter(mars_coords.iloc[:, 1], mars_coords.iloc[:, 0])
plt.title(r'Mars Craters plot for $\mathbf{N = 2000}$')
plt.xlabel(mars_coords.columns[1])
plt.ylabel(mars_coords.columns[0])
plt.savefig('n=2000_mars_craters.png', dpi=300)
plt.show()
plt.close('all')
del mars_coords

# grouping of the data
latitude_interval = np.linspace(-90, 90, 10)
longitude_interval = np.linspace(-180, 180, 10)

mars['latitude_cuts'] = pd.cut(mars.latitude_circle_image, latitude_interval,
                               include_lowest=True)
mars['longitude_cuts'] = pd.cut(mars.longitude_circle_image,
                                longitude_interval, include_lowest=True)

# use pandas built in functionality to create a observed contingency table
observed_results_table = pd.crosstab(mars.latitude_cuts, mars.longitude_cuts,
                                     margins=True)

# perform the chi squared test
chi2, p, dof, ex = scipy.stats.chi2_contingency(observed_results_table)
print('Overall chi2 test:\nchi2: {0:.1f}\np: {1:0.3f}\n'.format(chi2, p))

# holds  [-180, -140] and (20, 60] longitudes constant
# holds  (-70, -50] latitude constant
# iterates over all other latitudes to compare with the 'lower density' point
col_of_interest = 1
line_of_interest = 7
p_bonferoni_adjusted = 0.05/9
print('Bonferoni Adjusted P: {0:.3f}\n\n'.format(p_bonferoni_adjusted))
for enum_count, i in enumerate([0, 1, 2, 3, 4, 5, 6, 8, 9]):
    subset = observed_results_table.iloc[[i, line_of_interest], [0, 4]]
    chi2, p, dof, ex = scipy.stats.chi2_contingency(subset)
    print('Parwise test count: {3}\nPairwise chi2 test for:\n{0}.\n'
          'chi2: {1:.1f}\np: {2:0.3f}\nIs Null Hyphothesis rejected?'
          ' {4}\n'.format(subset, chi2, p, enum_count,
                          p < p_bonferoni_adjusted))


