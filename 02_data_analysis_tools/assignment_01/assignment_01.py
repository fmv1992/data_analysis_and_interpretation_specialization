import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi
import matplotlib.pyplot as plt

# reads the relevant data for this assignment
mars = pd.read_csv('02_mars_craters_study.csv', na_filter=True,
                   usecols=['DIAM_CIRCLE_IMAGE', 'DEPTH_RIMFLOOR_TOPOG'],
                   dtype=np.float64)
# cleans the data set
mars = mars.dropna()

# categorizing quantitative variable diameter of crater to
# 2.0 - 6.3 km -> big (contains upper range)
# 1.3 - 2.0 km -> medium (contains upper range)
# 1.0 - 1.3 km -> small (contains upper range)
# 0.0 - 1.0 km -> tiny (contains both extremes)
# tiny
is_tiny = (mars.DIAM_CIRCLE_IMAGE >= 0) & (mars.DIAM_CIRCLE_IMAGE <= 1)
# small
is_small = (mars.DIAM_CIRCLE_IMAGE > 1) & (mars.DIAM_CIRCLE_IMAGE <= 1.3)
# medium
is_medium = (mars.DIAM_CIRCLE_IMAGE > 1.3) & (mars.DIAM_CIRCLE_IMAGE <= 2.0)
# big
is_big = (mars.DIAM_CIRCLE_IMAGE > 2)
# initialize new column with a value which should be overriden
mars['CATEG_DIAM'] = False
# overrides the 'False' values with relevant names
for category, value in zip([is_tiny, is_small, is_medium, is_big],
                           ['tiny', 'small', 'medium', 'big']):
    pass
    mars.loc[:, 'CATEG_DIAM'].mask(category, other=value, inplace=True)
# checks the processing with arbitrary regions from the data set and a count
print(mars.head(), mars[180000:180005].copy(), mars.tail(),
      mars.loc[:, 'CATEG_DIAM'].value_counts(), '',
      sep=2 * '\n')

# The obtained values for mean and sd are:
# mean
mars_mean = mars.loc[:].groupby('CATEG_DIAM').aggregate(np.mean)
# I drop the diameter measure since this was the criteria for creating
# the categorical exploratory variables
mars_mean.drop('DIAM_CIRCLE_IMAGE', axis=1, inplace=True)
mars_mean.rename(columns={'DEPTH_RIMFLOOR_TOPOG':
                          'DEPTH_RIMFLOOR_TOPOG (average)'}, inplace=True)
# sd
mars_sd = mars.loc[:].groupby('CATEG_DIAM').aggregate(np.std)
# I drop the diameter measure since this was the criteria for creating
# the categorical exploratory variables
mars_sd.drop('DIAM_CIRCLE_IMAGE', axis=1, inplace=True)
mars_sd.rename(columns={'DEPTH_RIMFLOOR_TOPOG':
                        'DEPTH_RIMFLOOR_TOPOG (standard deviation)'},
               inplace=True)

# here I notice that the tiny group consists of only 1 km diameter craters
# therefore I proceed to remove them
mars_mean.drop('tiny', inplace=True)
mars_sd.drop('tiny', inplace=True)
mars = mars.loc[:].mask(is_tiny).dropna()
print('mean:\n', mars_mean, 2 * '\n', 'std dev pop:\n', mars_sd, sep='')

# we now proceed to the ANOVA test:
model1 = smf.ols(formula='DEPTH_RIMFLOOR_TOPOG ~ C(CATEG_DIAM)', data=mars)
results1 = model1.fit()
print(results1.summary())

# now the post hoc test:
mc1 = multi.MultiComparison(mars.loc[:, 'DEPTH_RIMFLOOR_TOPOG'],
                            mars.loc[:, 'CATEG_DIAM'])
res1 = mc1.tukeyhsd()
print(res1.summary(), flush=True)

# formats the plotting
plt.xlabel('DIAM_CIRCLE_IMAGE')
plt.ylabel('DEPTH_RIMFLOOR_TOPOG')
plt.scatter(mars.loc[:, 'DIAM_CIRCLE_IMAGE'],
            mars.loc[:, 'DEPTH_RIMFLOOR_TOPOG'])
plt.axis([0, 1200, 0, 6])
plt.show()

# code for the written part of the assignment
mars_count = mars.loc[:].groupby('CATEG_DIAM').aggregate(pd.DataFrame.count)
mars_count.drop('DIAM_CIRCLE_IMAGE', axis=1, inplace=True)
mars_count.rename(columns={'DEPTH_RIMFLOOR_TOPOG':
                           'COUNT'},
                  inplace=True)

mars_mean_sd_c = pd.concat([mars_mean, mars_sd, mars_count], axis=1, copy=True)
print(10 * '\n')
print('Results for the ANOVA test:', mars_mean_sd_c, results1.summary(),
      3 * '\n', sep='\n')
print('Results for the ad hoc test:', res1.summary(), sep='\n')
