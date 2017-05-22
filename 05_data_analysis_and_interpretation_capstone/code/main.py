"""Main file for Capstone project.

Coursera Course: Data Analysis and Interpretation Capstone.

    https://www.coursera.org/learn/data-analysis-capstone

This course is one in a series of: Data Analysis and Interpretation

Assignment: Capstone.
"""

import control
import zipfile
import io
import pandas as pd


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
    pass


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

    Arguments:
        dataframe (pandas.DataFrame): the dataframe to be managed.

    Returns:
        df (pandas.DataFrame): the managed dataframe
    """
    pass


def main():
    """Main function."""
    # Load and preprocess the dataframe.
    csv_file_obj = load_data(control.ZIP_PATH)
    treated_csv_file = pre_treat_data(csv_file_obj)
    df_original = pd.read_csv(treated_csv_file)
    del csv_file_obj, treated_csv_file
    df = df_original.copy(True)

    # Drop redundant columns
    df = df.drop(control.REDUNDANT_COLUMNS, axis=1)

    # Parse datetimes. (http://strftime.org/)
    parse_date_columns(df, columns=['begin_date_time', 'end_date_time'],
                       format='%d%b%y:%H:%M:%S')

    # Run debugger.
    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT  # noqa


if __name__ == '__main__':
    main()
