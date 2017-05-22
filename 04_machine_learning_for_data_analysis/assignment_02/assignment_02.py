u"""
Coursera Course: Machine Learning for Data Analysis.

    https://www.coursera.org/learn/machine-learning-data-analysis

This course is one in a series of: Data Analysis and Interpretation

Assignment 02: Random Forests.
"""

# pylama:ignore=C101,W0611

import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# sklearn imports
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import sklearn.metrics

from assignment_02_data_preparation import return_processed_diamonds_data_set
# The following function was abandoned.
# from assignment_02_data_preparation import create_price_histogram
import seaborn as sns


def main():
    u"""Main function for assignment 02."""
    # Load prepared data.
    df = return_processed_diamonds_data_set()
    # Mass is already included as mass in SI units.
    df.drop(['carat'], inplace=True, axis=1)

    # A bit of error checking.
    if df.isnull().sum().sum() != 0:
        raise ValueError('Your data has unintended nulls.')

    # A bit of data description. See histograms from assignment 01.
    # print('Data description:\n', df.describe())

    # Split into training and testing sets
    # The predictirs should not include any price variable since this was used
    # to create the output variable
    predictors = [x for x in df.columns.tolist() if 'price' not in x]
    print('Input variables:', predictors)
    input_variables = df[predictors]
    output_variable = df.price_expensive_binary.copy()  # Categorized price

    input_training, input_test, output_training, output_test = train_test_split(
        input_variables, output_variable, test_size=0.3, random_state=0)

    # Random forests and extra tree classifiers (extremely randomized trees) are
    # two ways of improving the bias-variance trade off

    # IN RANDOM FORESTS: 'each tree in the ensemble is built from a sample drawn
    # with replacement (i.e., a bootstrap sample) from the training set. In
    # addition, when splitting a node during the construction of the tree, the
    # split that is chosen is no longer the best split among all features.
    # Instead, the split that is picked is the best split among a random subset
    # of the features. As a result of this randomness, the bias of the forest
    # usually slightly increases (with respect to the bias of a single
    # non-random tree) but, due to averaging, its variance also decreases,
    # usually more than compensating for the increase in bias, hence yielding an
    # overall better model.'

    rf_classifier = RandomForestClassifier(
        n_estimators=400,
        max_depth=5,
        min_samples_split=500,
        min_samples_leaf=100,
        random_state=0,
        # verbose=True,
        n_jobs=-1)

    rf_classifier.fit(input_training, output_training)
    predictions = rf_classifier.predict(input_test)

    print('Random Forest')
    print('confusion matrix:\n:',
          sklearn.metrics.confusion_matrix(output_test, predictions))
    print('accuracy score:\n',
          sklearn.metrics.accuracy_score(output_test, predictions))
    rf_classifier.variable_feature_importances = dict(
        zip(predictors, rf_classifier.feature_importances_))

    # EXTREMELY RANDOMIZED TREES: In extremely randomized trees (see
    # ExtraTreesClassifier and ExtraTreesRegressor classes), randomness goes one
    # step further in the way splits are computed. As in random forests, a
    # random subset of candidate features is used, but instead of looking for
    # the most discriminative thresholds, thresholds are drawn at random for
    # each candidate feature and the best of these randomly-generated thresholds
    # is picked as the splitting rule. This usually allows to reduce the
    # variance of the model a bit more, at the expense of a slightly greater
    # increase in bias:

    er_classifier = ExtraTreesClassifier(
        n_estimators=400,
        max_depth=5,
        min_samples_split=500,
        min_samples_leaf=100,
        random_state=0,
        # verbose=True,
        n_jobs=-1)

    er_classifier.fit(input_training, output_training)
    predictions = er_classifier.predict(input_test)
    er_classifier.variable_feature_importances = dict(
        zip(predictors, er_classifier.feature_importances_))

    print('Extreme Classifier Tree')
    print('confusion matrix:\n:',
          sklearn.metrics.confusion_matrix(output_test, predictions))
    print('accuracy score:\n',
          sklearn.metrics.accuracy_score(output_test, predictions))
    print()

    return {'extreme': er_classifier,
            'random_forest': rf_classifier,
            'dataframe': df}


if __name__ == '__main__':
    result = main()
    etree, rforest = result['extreme'], result['random_forest']
    print('Random forest most important variables:',
          sorted(rforest.variable_feature_importances.items(),
                 key=lambda x: x[1], reverse=True))
    print()
    print('Extreme Random Tree most important variables:',
          sorted(etree.variable_feature_importances.items(),
                 key=lambda x: x[1], reverse=True))

    # From the results I got the impression that the 'y' variable could be
    # related to mass. Lets check that out:
    dataframe = result['dataframe']
    lm = sns.lmplot('y', 'mass',
                    data=dataframe,)
    axes = lm.axes
    axes[0, 0].set_ylim(-1, 1.1)
    axes[0, 0].set_xlim(-1, 15)
    plt.title('Scatter plot for diamond\'s width versus mass')
    plt.xlabel('Diamond width')
    plt.ylabel('Diamon mass')
    plt.tight_layout()
    plt.savefig('scatter_width_mass.png', dpi=500)
