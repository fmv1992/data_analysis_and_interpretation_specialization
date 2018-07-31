u"""
Coursera Course: Machine Learning for Data Analysis.

    https://www.coursera.org/learn/machine-learning-data-analysis


This course is one in a series of: Data Analysis and Interpretation

Assignment 03: Lasso Regression.
"""

# # pylama: skip=1
# pylama:ignore=C101,W0611

from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

# sklearn imports
from sklearn.model_selection import train_test_split
import sklearn.metrics
from sklearn import preprocessing
from sklearn.linear_model import LassoLarsCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_error

from assignment_03_data_preparation import return_proc_and_transf_data_set


def print_separator():
    u"""Prints a separator from between sections of text."""
    quantity = 50
    print(quantity * '-')
    return None


def main():
    u"""Main function for assignment 03."""
    # Load prepared data.
    df = return_proc_and_transf_data_set()
    # Mass is already included as mass in SI units.
    df.drop(['carat'], inplace=True, axis=1)
    # Those are dummy variables not needed in our data set anymore.
    df.drop(
        ['price_expensive', 'price_expensive_binary'],
        inplace=True, axis=1)

    # A bit of error checking.
    if df.isnull().sum().sum() != 0:
        raise ValueError('Your data has unintended nulls.')

    # Cast our dataframe into float type.
    df = df.astype('float64')

    # Scale our dataframe to avoid the sparsity control of our dataframe biased
    # against some variables.
    print('Prior to scaling:')
    print(df.describe())
    df = df.apply(preprocessing.scale)
    print('After scaling:')
    print(df.describe())
    print_separator()
    if (df.mean().abs() > 1e-3).sum() > 0:
        raise ValueError('Scaling of your dataframe went wrong.')

    # Split into training and testing sets
    # The predictirs should not include any price variable since this was used
    # to create the output variable
    predictors = [x for x in df.columns.tolist() if 'price' not in x]
    print('Input variables:')
    pprint(predictors, indent=4)
    input_variables = df[predictors].copy()
    output_variable = df.price.copy()  # Categorized price
    print_separator()

    input_training, input_test, output_training, output_test = train_test_split(
        input_variables, output_variable, test_size=0.3, random_state=0)

    # A few words about the LassoLarsCV:

    # LASSO: least absolute shrinkage and selection operator (discussed in
    # the course material.

    # LARS: least angle regression: algorithm for linear regression models
    # to high-dimensional data (aka 'a lot of categories').
    # Compared to simple LASSO this model uses the LARS algorithm instead of
    # the 'vanilla' 'coordinate_descent' of simple LASSO.

    # CV: cross validation: this sets the alpha parameter (refered to as
    # lambda parameter in the course video) by cross validation.
    # In the simple LARS this alpha (the penalty factor) is an input of the
    # function.
    # 'The alpha parameter controls the degree of sparsity of the
    # coefficients estimated.
    # If alpha = zero then the method is the same as OLS.

    model = LassoLarsCV(
        cv=10,  # Number of folds.
        precompute=False,  # Do not precompute Gram matrix.
        # precompute=True,  # Do not precompute Gram matrix.
        # verbose=3,
    ).fit(input_training, output_training)

    dict_var_lin_coefs = dict(zip(
        predictors,
        model.coef_))

    print('Result of linear model:')
    pprint(sorted([(k, v) for k, v in dict_var_lin_coefs.items()],
                  key=lambda x: abs(x[1]))
           )
    print_separator()

    # Plot coefficient progression.
    # TODO: plot those on 4 different subplots.
    model_log_alphas = -np.log10(model.alphas_)
    ax = plt.gca()
    plt.plot(model_log_alphas, model.coef_path_.T)
    plt.axvline(-np.log10(model.alpha_), linestyle='--', color='k',
                label='alpha CV')
    plt.ylabel('Regression Coefficients')
    plt.xlabel('-log(alpha)')
    plt.title('Regression Coefficients Progression for Lasso Paths')
    plt.legend(predictors,
               loc='best',)
    plt.tight_layout()
    plt.savefig('result00.png', dpi=600)
    plt.close()
    # TODO: why are the coefficients in the result very different than the
    # coefficient path?
    #
    # There seems to be a scaling of the coefficient paths with an arbitrary
    # almost the same constant (194 in this case)
    #
    # print('Resulting alpha is not different than path alpha (difference):')
    # difference = model.alpha_ - model.alphas_
    # pprint(model.alpha_ - model.alphas_)
    # print('Resulting coefficients are very different than path coefficients (difference):')
    # pprint(model.coef_ - model.coef_path_.T)
    # print_separator()

    # Plot mean square error for each fold.
    # To avoid getting dividebyzero warning map zero to an extremely low value.
    model.cv_alphas_ = list(
        map(lambda x: x if x != 0 else np.inf,
            model.cv_alphas_))
    model_log_alphas = -np.log10(model.cv_alphas_)
    plt.figure()
    plt.plot(model_log_alphas, model.cv_mse_path_, ':')
    plt.plot(model_log_alphas, model.cv_mse_path_.mean(axis=-1), 'k',
             label='Average across the folds', linewidth=2)
    plt.axvline(-np.log10(model.alpha_), linestyle='--', color='k',
                label='alpha CV')
    plt.xlabel('-log(alpha)')
    plt.ylabel('Mean squared error')
    plt.title('Mean squared error on each fold')
    plt.legend()
    plt.tight_layout()
    plt.savefig('result01.png', dpi=600)
    plt.close()

    # Mean squared error of our model.
    train_error = mean_squared_error(output_training,
                                     model.predict(input_training))
    test_error = mean_squared_error(output_test,
                                    model.predict(input_test))
    print('Training data MSE')
    print(train_error)
    print('Test data MSE')
    print(test_error)
    print_separator()

    # R-square from training and test data.
    rsquared_train = model.score(
        input_training,
        output_training)
    rsquared_test = model.score(
        input_test,
        output_test)
    print('Training data R-square')
    print(rsquared_train)
    print('Test data R-square')
    print(rsquared_test)
    print_separator()

    return {'model': model, 'dataframe': df}


if __name__ == '__main__':
    main()
