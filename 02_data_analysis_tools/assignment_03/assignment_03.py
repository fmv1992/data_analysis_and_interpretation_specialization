# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 07:41:45 2016

@author: e061568
"""
import pandas as pd
import scipy
import seaborn
import matplotlib.pyplot as plt
import itertools
import scipy.stats

# importing and cleaning of the database
gapminder = pd.read_csv('04_gapminder_quantitative.csv', index_col='country')
gapminder.rename(index=lambda x: str(x).lower(), inplace=True)
gapminder.dropna(inplace=True)

# doing all combinations and sorting
list_of_max_pearsons = []
for c1, c2 in itertools.combinations(gapminder.columns, 2):
    pearson_r, p_value_two_tails = scipy.stats.pearsonr(gapminder[c1],
                                                       gapminder[c2])
    list_of_max_pearsons.append((pearson_r, c1, c2, p_value_two_tails))
list_of_max_pearsons.sort(key=lambda x: x[0], reverse=True)

# taking some interesting values
pearson_r_max, c1_max, c2_max, p_max = list_of_max_pearsons[0]
pearson_r_max_2, c1_max_2, c2_max_2, p_max_2 = list_of_max_pearsons[1]
pearson_r_zero, c1_zero, c2_zero, p_zero = list_of_max_pearsons[70]
pearson_r_min, c1_min, c2_min, p_min = list_of_max_pearsons[-1]

# saving the plots into figures: 2 maximum pearsons r for GapMinder
plt.figure(1)
plt.subplot(2,1,1)
plt.xlabel(c1_max)
plt.ylabel(c2_max)
plt.text(20000, 0, (r'$r_{{pearson}}={0:0.3f}${2}'
                    '$r_{{pearson}}^2={1:0.3f}$').format(
                    pearson_r_max, pearson_r_max ** 2, '\n',),
bbox={'facecolor':'white'})
plt.title('1st Maximum Pearson\'s linear correlation for Gapminder Data Set')
plt.scatter(gapminder[c1_max], gapminder[c2_max])
plt.subplot(2,1,2)
plt.scatter(gapminder[c1_max_2], gapminder[c2_max_2])
plt.xlabel(c1_max_2)
plt.ylabel(c2_max_2)
plt.text(0, 6000, (r'$r_{{pearson}}={0:0.3f}${2}'
                   '$r_{{pearson}}^2={1:0.3f}$').format(
                   pearson_r_max_2, pearson_r_max_2 ** 2, '\n'),
bbox={'facecolor':'white'})
plt.title('2nd Maximum Pearson\'s linear correlation for Gapminder Data Set')
plt.tight_layout()
plt.savefig('first_and_second_highest_pearsons_correlations.png', dpi=500)
plt.close(1)
print('pearsons r: {0:0.3f}\npearsons r²: {1:0.3f}\np-value: {4:0.3f}\n'
      'for {2} and {3} data sets\n\n'.format(
pearson_r_max, pearson_r_max ** 2, c1_max, c2_max, p_max
))
print('pearsons r: {0:0.3f}\npearsons r²: {1:0.3f}\np-value: {4:0.3f}\n'
      'for {2} and {3} data sets\n\n'.format(
pearson_r_max_2, pearson_r_max_2 ** 2, c1_max_2, c2_max_2, p_max_2
))

# saving the plots into figures: r_pearson ~ 0
plt.figure(2)
plt.xlabel(c1_zero)
plt.ylabel(c2_zero)
plt.text(2.5e11, 30, (r'$r_{{pearson}}={0:0.3f}${2}'
                      '$r_{{pearson}}^2={1:0.3f}$').format(
pearson_r_zero, pearson_r_zero ** 2, '\n',
),
bbox={'facecolor':'white'})
plt.title('Almost zero Pearson\'s $r$')
plt.scatter(gapminder[c1_zero], gapminder[c2_zero])
plt.tight_layout()
plt.savefig('pearsons_correlation_almost_zero.png', dpi=500)
plt.close(2)
print('pearsons r: {0:0.3f}\npearsons r²: {1:0.3f}\np-value: {4:0.3f}\n'
      'for {2} and {3} data sets\n\n'.format(
pearson_r_zero, pearson_r_zero ** 2, c1_zero, c2_zero, p_zero
))

# saving the plots into figures: r_pearson_min
plt.figure(2)
plt.xlabel(c1_min)
plt.ylabel(c2_min)
plt.text(10, 80, (r'$r_{{pearson}}={0:0.3f}${2}'
                  '$r_{{pearson}}^2={1:0.3f}$').format(
pearson_r_min, pearson_r_min ** 2, '\n',
), bbox={'facecolor':'white'})
plt.title('Pearson\'s lowest $r$ for GapMinder')
plt.scatter(gapminder[c1_min], gapminder[c2_min])
plt.tight_layout()
plt.savefig('pearsons_lowest_correlation.png', dpi=500)
plt.close(2)
print('pearsons r: {0:0.3f}\npearsons r²: {1:0.3f}\np-value: {4:0.3f}\n'
      'for {2} and {3} data sets\n\n'.format(
pearson_r_min, pearson_r_min ** 2, c1_min, c2_min, p_min
))