"""Main file for Capstone project.

Coursera Course: Data Analysis and Interpretation Capstone.

    https://www.coursera.org/learn/data-analysis-capstone

This course is one in a series of: Data Analysis and Interpretation

Assignment: Capstone.
"""

import control
import zipfile
import numpy as np
import io
import os
import pandas as pd
import matplotlib.pyplot as plt
from data_utilities import python_utilities as pyu
from data_utilities import pandas_utilities as pu
from data_utilities import matplotlib_utilities as mu


def load_data(zippath):
    """Load the data from a zippath and return a file object."""
    with zipfile.ZipFile(zippath, 'r') as zipfileobj:
        zip_file_list = zipfileobj.namelist()
        if len(zip_file_list) == 1:
            with zipfileobj.open(zip_file_list[0], 'r') as csvfile:
                return io.StringIO(csvfile.read().decode('utf8'))


def pre_treat_data(fileobj):
    """Pre treat the data before loading into a dataframe."""
    treated_data = fileobj.read().lower()
    return io.StringIO(treated_data)


def report_and_understand_nans(dataframe):
    """Help understanding if there are any patterns in dataset's nans."""
    bin_null_df = dataframe.isnull()
    pyu.print_feature('Understanding NANs')
    # Investigate nans distribution.
    total_nans = bin_null_df.sum().sum() / (dataframe.shape[0] *
                                            dataframe.shape[1])
    print('Total nans: {0:1.1%}'.format(total_nans))
    # Nans distribution per columns.
    per_col_nans = bin_null_df.sum() / bin_null_df.sum().sum()
    per_col_nans = per_col_nans[per_col_nans != 0].sort_values()
    print('Concentrated in columns as such: \n{0}'.format(per_col_nans))
    # Plot hexbin.
    # Gather data for the hexbin.
    x_es = []
    y_es = []
    for i, c in enumerate(bin_null_df.columns):
        mask = bin_null_df.loc[:, c] == True
        y = mask.index
        x = np.ones_like(y) * i
        x_es.append(x)
        y_es.append(y)
    x = np.array(x_es).flatten()
    y = np.array(y_es).flatten()
    fig = plt.figure()
    # Plot the hexbin.
    hexbin = plt.hexbin(x, y, gridsize=25)  # noqa
    # Add a colorbar.
    # cb = plt.colorbar()  # noqa
    # Save figure.
    fig.savefig(
        os.path.join(control.OUTPUT_PATH, 'heatmap.png'),
        dpi=300)


def parse_date_columns(dataframe, columns=[], format=''):
    """Parse datetime columns in dataframe."""
    # Formats in http://strftime.org/.
    for col in columns:
        dataframe.loc[:, col] = pd.to_datetime(dataframe.loc[:, col],
                                               format='%d%b%y:%H:%M:%S')
        # dataframe.drop(col, axis=1, inplace=True)
    return None


def manage_dataset(dataframe):
    """Manage the data in the dataframe.

    In order to manage:
        * all the columns must be lower_case_underscore_separated_names.
        * all nans should be either filled or dropped
        * all redundant variables must be dropped (especially the date/time
        variables).
        * all measure units must be in SI

    Arguments:
        dataframe (pandas.DataFrame): the dataframe to be managed.

    Returns:
        df (pandas.DataFrame): the managed dataframe
    """
    # Drop redundant variables.
    dataframe = dataframe.drop(control.REDUNDANT_COLUMNS, axis=1)

    # Rename variables to be renamed.
    dataframe.rename(columns=control.RENAME_COLUMNS, inplace=True)

    # Drop entries which have absence of out response variables.
    # In order to investigate losses we will reduce the dataframe for which
    # weather phenomena have damages and injuries/deaths reported.
    relevant_columns = dataframe.loc[:, control.RELEVANT_COLUMNS]
    relevant_index = relevant_columns.notnull().all(axis=1)
    dataframe = dataframe[relevant_index]

    # Do unit conversion.
    dataframe.loc[:, 'tor_length'] = (dataframe.loc[:, 'tor_length']
                                      * control.MILES_TO_M)
    dataframe.loc[:, 'tor_width'] = (dataframe.loc[:, 'tor_width']
                                     * control.FEET_TO_M)

    # Parse damage as values.
    for damage_col in control.DAMAGE_COLUMNS:
        # not_null = dataframe.loc[:, damage_col].notnull()
        d = dataframe.loc[:, damage_col]
        is_k_column = d.str.endswith('k').fillna(False)
        is_m_column = d.str.endswith('m').fillna(False)
        is_b_column = d.str.endswith('b').fillna(False)
        multiplier = (1e3 * is_k_column
                      + 1e6 * is_m_column
                      + 1e9 * is_b_column)
        # import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
        # is_k_column = (not_null & is_k_column)
        # is_m_column = (not_null & is_m_column)
        dataframe.loc[:, damage_col] = (d.str.slice(0, -1).astype('float')
                                        * multiplier)

    # Create a total damage columns.
    dataframe['damage_total'] = (dataframe['damage_crops']
                                 + dataframe['damage_property'])

    return dataframe


def do_exploratory_analysis(dataframe):
    """Execute exploratory analysis on the dataframe."""
    # Drop duplicate column for this analysis.
    df = dataframe.drop('end_date_time', axis=1)
    columns = df.columns.copy()
    # Expand dataframe.
    expanded_df = pd.concat(
        (df,
         df.begin_date_time.dt.hour,
         df.begin_date_time.dt.day,
         df.begin_date_time.dt.month,
         df.begin_date_time.dt.year),
        axis=1,
    )
    expanded_df.columns = (columns.tolist()
                           + ['begin_date_' + x for x in
                              ('hour', 'day', 'month', 'year')])

    # Histogram each column.

    numeric_cols = sorted(pu.get_numeric_columns(expanded_df))
    non_numeric_cols = sorted(set(expanded_df.columns.tolist())
                              - set(numeric_cols))
    filled_df = pd.concat(
        map(lambda x: x.reset_index(),
            (expanded_df[numeric_cols].fillna(-1),
             expanded_df[non_numeric_cols]  # Already filled with 'nan'.
             )),
        axis=1).drop('index', axis=1)
    assert filled_df.shape == expanded_df.shape
    mu.histogram_of_dataframe(filled_df,
                              output_path='../output/exploratory_analyses',
                              kde=False,
                              )
    return None


def main():
    """Main function."""
    # Load and preprocess the dataframe.
    csv_file_obj = load_data(control.ZIP_PATH)
    treated_csv_file = pre_treat_data(csv_file_obj)
    df_original = pd.read_csv(treated_csv_file)
    del csv_file_obj, treated_csv_file
    df = df_original.copy(True)

    # Manage data set.
    df = manage_dataset(df)

    # Transform object columns to category.
    df = pu.object_columns_to_category(df, inplace=False)

    # Parse datetimes. (http://strftime.org/)
    parse_date_columns(df, columns=['begin_date_time', 'end_date_time'],
                       format='%d%b%y:%H:%M:%S')

    # Drop remaning object columns.
    obj_cols = [x for x in df if str(df[x].dtype) == 'object']
    df = df.drop(obj_cols, axis=1)

    # Understand Nans.
    # report_and_understand_nans(df)  # TODO: release me

    # Execute exploratory_analysis.
    do_exploratory_analysis(df)

    # Run debugger.
    # import ipdb; ipdb.set_trace()  # XXX BREAKPOINT  # noqa


if __name__ == '__main__':
    main()
