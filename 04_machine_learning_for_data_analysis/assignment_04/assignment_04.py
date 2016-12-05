u"""
Coursera Course: Machine Learning for Data Analysis.

    https://www.coursera.org/learn/machine-learning-data-analysis


This course is one in a series of: Data Analysis and Interpretation

Assignment 04: K-Means cluster analysis.
"""

# pylama:ignore=C101,W0611,W0612,R0914

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
# sklearn imports.
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
# scipy imports
from scipy.spatial.distance import cdist
# statsmodels imports
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi

# Local imports.
import assignment_04_data_preparation


def print_separator():
    u"""Print a separator from between sections of text."""
    quantity = 50
    print(quantity*'-')
    return None


def main():
    u"""Main function for assignment 03."""
    # Load prepared data.
    df = assignment_04_data_preparation.return_processed_diamonds_data_set()
    price_series = df.price.copy()
    # Drop variables:
    #   1) Related to price. This will be our analyzed variable.
    #   2) Cut (quality) since it is a result of human assessment.
    df.drop(['price_expensive',
             'price_expensive_binary',
             'price',
             # 'cut',
             'depth',
             'table',
             ],  # noqa
            axis=1,
            inplace=True)

    # Data management: data set has no nulls.
    if df.isnull().sum().sum() != 0:
        raise ValueError('Your data has unintended nulls.')

    # There is a need to preserve the original data frame since we will look
    # into the average of the original variables:
    df_original = df.copy()
    # Data normalization and casting.
    for num_col in df.columns.tolist():
        df[num_col] = preprocessing.scale(df[num_col].astype('float64'))
    # print(df.describe())
    # print_separator()

    # Split data into training and test sets. In this case since it makes no
    # sense to split the data into training and test set we delete the (empty)
    # test set.
    cluster_training_set, cluster_test_set = train_test_split(
        df,
        test_size=0.0,
        random_state=1)
    del cluster_test_set

    # Decide upon a cluster number for the K-Mean clusterization.
    cluster_nr = range(1, 10)
    mean_distances = []
    # A cluster will have a number of points. Each of the data set point has a
    # distance to each of these points. Nevertheless only the minimum distance
    # of a data set point to a 'mean point' should be considered for calculation
    # in the mean distance.
    for k_clusters in cluster_nr:
        model = KMeans(
            n_clusters=k_clusters,
            random_state=1,
            # max_iter=1000,
            # n_jobs=3,
        )
        model.fit(cluster_training_set)
        cluster_prediction = model.predict(cluster_training_set)
        # Calculate the mean distance of each set of point to the clusters.
        distances = cdist(cluster_training_set,
                          model.cluster_centers_,
                          metric='euclidean')
        # With axis = 1 get the minimum distance of a point to a cluster and not
        # the absolute minimum distance.
        # In the end each point as a distance attributed to it (the minimum
        # one). This attribute can also be acessed by the 'inertia_' property.
        min_distance = np.min(distances, axis=1)
        average_of_min_distances = (np.sum(min_distance)
                                    / cluster_training_set.shape[0])  # noqa
        # The
        mean_distances.append(average_of_min_distances)
        # print('cluster_centers', model.cluster_centers_)
        # print('mean_distance', mean_distance)
        # print('min_distance', mean_distance)

    # Plot clusters mean distance.
    ax = plt.gca()
    ax.plot(cluster_nr, mean_distances)
    plt.xlabel('Number of clusters')
    plt.ylabel('Average distances')
    plt.title('Selecting k with the Elbow Method')
    # Plot a circle showing the point.
    N_CLUSTERS = 3
    selecting_circle = plt.Circle(
        (N_CLUSTERS, mean_distances[N_CLUSTERS-1]),
        0.1,
        color='r',
        fill=False,
        # linewidth=,
        )  # noqa
    ax.add_artist(selecting_circle)
    plt.savefig('n_clusters_versus_average_dist.png', dpi=500)
    plt.close('all')
    # Print result of selected number of elbows.
    print('Selected n = 3 clusters')
    print_separator()

    # Create a solution with 3 clusters
    model = KMeans(
        n_clusters=N_CLUSTERS,
        random_state=1
    )
    model.fit(cluster_training_set)
    cluster_assignment = model.predict(cluster_training_set)

    # Principal Component Analysis: convert a set of possibly correlated
    # varibles into a set of linearily uncorrelated variables.
    pca2 = PCA(2)
    pca_coordinates = pca2.fit_transform(cluster_training_set)
    x = pca_coordinates[:, 0]
    y = pca_coordinates[:, 1]
    ax = plt.gca()
    ax.scatter(x, y, c=model.labels_)
    plt.xlabel('Canonical variable 1')
    plt.ylabel('Canonical variable 2')
    plt.title('Scatterplot of Canonical Variables for 3 Clusters')
    plt.savefig('clusters_on_canonical_variables.png', dpi=500)
    plt.close('all')

    # Do we use the test set for the k-means clustering?
    # According to
    # http://stackoverflow.com/questions/13394478/why-we-need-training-and-test-datasets-in-research
    # which makes sense, there no test set in clustering analisys.
    #
    # Include price in the data frame and analyze the average price of diamonds
    # in each cluster.
    # It is worth saying that the original data frame must be restored here in
    # order for its mean and non-normalized/non-scaled values to have meaningful
    # value.
    df_clustered = df_original.copy()
    df_clustered['price'] = price_series
    df_clustered['clusters'] = model.labels_

    # Now group by cluster.
    clustergb = df_clustered.groupby('clusters').mean()
    print("Clustering variable means by cluster:")
    print(df_clustered.groupby('clusters').mean())
    print('Standard deviation of price by cluster:')
    print(df_clustered.groupby('clusters').std())
    print_separator()

    # Test the correlation of price variable to each cluster.
    price_ols_fit = smf.ols(
        formula='price ~ C(clusters)',
        data=df_clustered).fit()
    print('Ordinary least squares regression for price versus clusters:')
    print(price_ols_fit.summary())
    print_separator()

    multi_comparison = multi.MultiComparison(
        df_clustered['price'],
        df_clustered['clusters'])
    result = multi_comparison.tukeyhsd()
    print(result.summary())
    print_separator()

    return {
        'training_set': cluster_training_set,
        'dataframe': df,
        'model': model,
    }


if __name__ == '__main__':
    main()
