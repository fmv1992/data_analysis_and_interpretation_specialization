# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 08:17:14 2016

@author: monteiro
"""
import pandas as pd  # version '0.18.0'
import seaborn  # version '0.7.0'
import matplotlib.pyplot as plt  # version'1.3.1'
import scipy.stats

db = pd.read_csv('03_national_longitudinal_study_of_adolescent_health_'
                 'addhealth_subset.csv', low_memory=False, index_col='id')

db['does_great_exact_sciences'] = False
db['does_great_human_sciences'] = False
db['is_happy_at_school'] = False

db.loc[((db.grade_math == True) & (db.grade_science == True)),
       'does_great_exact_sciences'] = True

db.loc[((db.grade_language_arts == True) &
        (db.grade_history_social_studies == True)),
       'does_great_human_sciences'] = True

db.loc[((db.happy_at_school == 1) | (db.happy_at_school == 2)),
        'is_happy_at_school'] = True

cross_tab_exact = pd.crosstab(index=db.is_happy_at_school,
                              columns=[db.does_great_exact_sciences],
                              margins=True)

# displays the cross tabulation without moderation
print('First cross tabulation: performance on exact sciences and happiness '
'at school:')
print(cross_tab_exact)
print('Percent of happy students who do great in exact sciences and '
      'are happy: {0:0.1%}\nPercent of happy students overall: '
      '{1:0.1%}\n\n'.format(
    cross_tab_exact.loc[True, True]/cross_tab_exact.loc['All', True],
    cross_tab_exact.loc[True, 'All']/cross_tab_exact.loc['All', 'All'],)
                           )

# displays the cross tabulation with moderation
cross_tab_full = pd.crosstab(index=db.is_happy_at_school,
            columns=[db.does_great_exact_sciences,
                     db.does_great_human_sciences],
            margins=True)
print('Second cross tabulation: performance on exact sciences, human sciences'
      ' and happiness at school:')
print(cross_tab_full)
print('Percent of happy students who do great in exact sciences and human'
      ' sciences and are happy: {0:0.1%}\n'
      'Percent of happy students who do great in exact sciences but '
      'NOT in human sciences and are happy: {2:0.1%}\n'
      'Percent of happy students overall: {1:0.1%}\n\n'.format(
    cross_tab_full.loc[True, (True, True)]/cross_tab_full.loc['All',
                                                              (True, True)],
    float(cross_tab_full.loc[True, 'All']/cross_tab_full.loc['All', 'All']),
    cross_tab_full.loc[True, (True, False)]/cross_tab_full.loc['All',
                                                               (True, False)]
                                                               )
     )

# removes sub totals from cross tabulations to do a chi squared analysis
cross_tab_exact = cross_tab_exact.iloc[:-1, :-1]
cross_tab_full = cross_tab_full.iloc[:-1, :-1]

# does the chi squared test
chi1, p1, dof1, expected1 = scipy.stats.chi2_contingency(cross_tab_exact)
print('Original group: happiness and doing great in exact sciences:\n\tchi '
      'squared: {0:2f}\n\tp-value: {1:1.4f}\n\n'.format(chi1, p1))

# does the chi squared test for polymaths
chi2, p2, dof2, expected2 = scipy.stats.chi2_contingency(
    cross_tab_full.loc[:, (slice(None), True)])
print('Moderated group: happiness and doing great in exact sciences and '
      'doing great in human sciences:\n\tchi squared: '
      '{0:2f}\n\tp-value: {1:1.4f}'.format(chi2, p2))
print(cross_tab_full.loc[:, (slice(None), True)], '\n\n')

chi3, p3, dof3, expected3 = scipy.stats.chi2_contingency(
    cross_tab_full.loc[:, (slice(None), False)])
print('Moderated group: happiness and doing great in exact sciences and '
      'NOT doing great in human sciences:\n\tchi squared: '
      '{0:2f}\n\tp-value: {1:1.4f}'.format(chi3, p3))
print(cross_tab_full.loc[:, (slice(None), False)])
