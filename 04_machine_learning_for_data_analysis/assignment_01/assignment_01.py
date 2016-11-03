u"""
Coursera Course: Machine Learning for Data Analysis.

    https://www.coursera.org/learn/machine-learning-data-analysis


This course is one in a series of: Data Analysis and Interpretation

Assignment 01: Decision Trees.
"""

# # pylama: skip=1
# pylama:ignore=C101,W0611

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import sklearn.metrics
from assignment_01_data_preparation import return_processed_diamonds_data_set
import seaborn
import pydotplus
from IPython.display import Image
from io import StringIO
from sklearn import tree


def main():
    u"""Main function for assignment 01."""
    df = return_processed_diamonds_data_set()

    if df.isnull().sum().sum() != 0:
        raise ValueError('Your data has unintended nulls.')

    df.describe()

    # Split into training and testing sets
    input_variables = df[['cut', 'color', 'clarity', 'mass']]
    output_variable = df.price_expensive_binary  # Categorized price

    input_training, input_test, output_training, output_test = train_test_split(
        input_variables, output_variable, test_size=0.3, random_state=0)

    # Build model on training data
    tree_classifier = DecisionTreeClassifier(
        max_depth=4,
        min_samples_split=1000,
        random_state=0,  # This is to keep data reproducible.
    )

    tree_classifier = tree_classifier.fit(input_training, output_training)

    predictions = tree_classifier.predict(input_test)

    print('conf matrix', sklearn.metrics.confusion_matrix(output_test,
                                                          predictions))
    print('accuracy', sklearn.metrics.accuracy_score(output_test, predictions))

    # Displaying the decision tree
    # from StringIO import StringIO
    # from StringIO import StringIO
    # from IPython.display import Image
    # out = StringIO()
    # tree.export_graphviz(classifier, out_file=out)
    # import pydotplus
    # graph=pydotplus.graph_from_dot_data(out.getvalue())
    # Image(graph.create_png())

    out = StringIO()
    tree.export_graphviz(
        tree_classifier,
        out_file=out,
        feature_names=input_variables.columns.tolist(),
        class_names=['cheap', 'expensive'],
        filled=True,
        impurity=True,)
    graph = pydotplus.graph_from_dot_data(out.getvalue())
    with open('graph.png', 'wb') as f:
        f.write(graph.create_png())

    # Histogram of Clarity Variable
    plt.figure(0)
    df.clarity.value_counts(sort=False).plot.bar()
    plt.title('Histogram of Clarity values (0: least clear)')
    plt.tight_layout()
    plt.savefig('diamonds_clarity_histogram.png', dpi=500)
    plt.close()

    # Histogram of Cut Variable
    plt.figure(0)
    df.cut.value_counts(sort=False).plot.bar()
    plt.title('Histogram of Cut values (4: ideal)')
    plt.tight_layout()
    plt.savefig('diamonds_cut_histogram.png', dpi=500)
    plt.close()

    # Histogram of Color Variable
    plt.figure(0)
    df.color.value_counts(sort=False).plot.bar()
    plt.title('Histogram of Color values (0: worst)')
    plt.tight_layout()
    plt.savefig('diamonds_color_histogram.png', dpi=500)
    plt.close()

    # Histogram of the mass Variable
    plt.figure(0)
    df.mass.plot.hist()
    plt.title('Mass of the diamong (kg)')
    plt.tight_layout()
    plt.savefig('diamonds_mass_histogram.png', dpi=500)
    plt.close()

    return df


if __name__ == '__main__':
    main()
