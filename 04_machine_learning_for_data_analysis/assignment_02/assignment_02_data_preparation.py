"""
Data preparation for assignment 02.

Prepares the diamond database found in

https://vincentarelbundock.github.io/Rdatasets/datasets.html

Some categorical variables are mapped to integers ranging from:
    0: worst value in that categorical
    ...
    max: best value in that categorical

"""

import os

# pylama:ignore=W0611
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from project_library import DATASETS_PATH


def return_processed_diamonds_data_set():
    u"""Main function. Return processed diamonds dataset."""
    # Set constants
    CSVPATH = os.path.join(DATASETS_PATH, 'diamonds.csv')
    DTYPES = {
        'carat': np.float64,
        'cut': pd.Categorical,
        'color': pd.Categorical,
        'clarity': pd.Categorical,
        'depth': np.float64,
        'table': np.float64,
        'price': np.int64,
        'x': np.float64,
        'y': np.float64,
        'z': np.float64,
    }
    PRICE_QUANTILE = 0.75

    # Load data set.
    df = pd.read_csv(CSVPATH, index_col=0, dtype=DTYPES)

    # Categorize expensive, medium or cheap (our output variable).
    is_expensive = df.price > df.price.quantile(PRICE_QUANTILE)
    df['price_expensive'] = pd.Categorical.from_codes(
        is_expensive,
        categories=['cheap', 'expensive'])
    df['price_expensive_binary'] = df.price_expensive.map(
        {'expensive': 1, 'cheap': 0})

    # Helper to categorize the clarity.
    clarity_map = {
        'I1': 0,    # Least clear
        'SI1': 1,
        'SI2': 2,
        'VS1': 3,
        'VS2': 4,
        'VVS1': 5,
        'VVS2': 6,
        'IF': 7,    # Most clear
    }
    df.replace(to_replace={'clarity': clarity_map}, inplace=True)

    # Helper to categorize color.
    # 0 is the worst color (J)
    # 6 is the best color (D)
    df.color = df.color.apply(lambda x: ord('j') - ord(x.lower()))

    # Helper to categorize cut
    df.cut = df.cut.apply(str.lower)
    CUT_SCALE = {
        'fair': 0,
        'good': 1,
        'very good': 2,
        'premium': 3,
        'ideal': 4,
    }
    df.replace(to_replace={'cut': CUT_SCALE}, inplace=True)

    # Creates a column with SI mass
    CARAT_TO_KG = 200e-3
    df['mass'] = df.carat * CARAT_TO_KG

    # Gives a nice description for each variable.
    description = {
        'price': 'price in US dollars (\$326–\$18,823)',
        'carat': 'weight of the diamond (0.2–5.01)',
        'cut': 'quality of the cut (Fair, Good, Very Good, Premium, Ideal)',
        'colour': 'diamond colour, from J (worst) to D (best)',
        'color': 'diamond colour, from J (worst) to D (best)',
        'clarity': 'a measurement of how clear the diamond is (I1 (worst), '
            'SI1, SI2, VS1, VS2, VVS1, VVS2, IF (best))',  # noqa
        'x': 'length in mm (0–10.74)',
        'y': 'width in mm (0–58.9)',
        'z': 'depth in mm (0–31.8)',
        'depth': 'total depth percentage = z / mean(x, y) = 2 * z / (x + y) '
            '(43–79)',  # noqa
        'table': 'width of top of diamond relative to widest point (43–95)',
    }
    df.variable_description = description

    return df


# def create_price_histogram(df, fname='diamonds_price_histogram.png'):
#     u"""Create a histogram for diamond prices.
#
#     Create a histogram for diamond prices to enable classification of price
#     ranges.
#
#     Arguments:
#         df (Dataframe): The dataframe which has the price column.
#
#     Returns:
#         bool: True if successful. False otherwise.
#
#     """
#     # print(df.price.describe())
#     plt.cla()
#     plt.close('all')
#     plt.figure(1)
#     xticks_range = range(0, 20000, 1000)
#     price_plot = sns.distplot(df.price, rug=False, kde=False)
#     price_plot.set(
#         xticks=xticks_range,
#         title='title',  # TODO
#     )
#     price_plot.set_xticklabels(labels=price_plot.get_xticks(),
#                                rotation=90)
#     plt.tight_layout()
#     plt.savefig(fname, dpi=500)
#     plt.close('all')
#     return True

if __name__ == '__main__':
    return_processed_diamonds_data_set()
