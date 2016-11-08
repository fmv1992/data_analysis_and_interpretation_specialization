u"""
Coursera Course: Machine Learning for Data Analysis.

    https://www.coursera.org/learn/machine-learning-data-analysis


This course is one in a series of: Data Analysis and Interpretation

Assignment 02: Random Forests.
"""

# # pylama: skip=1
# pylama:ignore=C101,W0611

import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# sklearn imports
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import sklearn.metrics

from assignment_02_data_preparation import return_processed_diamonds_data_set
from assignment_02_data_preparation import create_price_histogram
import seaborn


def main():
    u"""Main function for assignment 01."""
    # Load prepared data.
    df = return_processed_diamonds_data_set()
    create_price_histogram(df)
    # raise Exception

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

    classifier = RandomForestClassifier(
        n_estimators=400,
        max_depth=5,
        min_samples_split=500,
        min_samples_leaf=100,
        random_state=0,
        # verbose=True,
        n_jobs=-1)

    classifier.fit(input_training, output_training)
    predictions = classifier.predict(input_test)

    print('Random Forest')
    print('confusion matrix:\n:',
          sklearn.metrics.confusion_matrix(output_test, predictions))
    print('accuracy score:\n',
          sklearn.metrics.accuracy_score(output_test, predictions))

    return df


if __name__ == '__main__':
    main()
