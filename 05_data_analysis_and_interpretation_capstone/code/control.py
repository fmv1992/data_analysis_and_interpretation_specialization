"""Control file for Capstone project.

Contains the constants and important variables for this assignment.

Coursera Course: Data Analysis and Interpretation Capstone.

    https://www.coursera.org/learn/data-analysis-capstone

This course is one in a series of: Data Analysis and Interpretation

Assignment: Capstone.
"""
import os

# Path variables.
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_PATH, 'data')
ZIP_PATH = os.path.join(DATA_PATH, 'storm_event_data.zip')
OUTPUT_PATH = os.path.join(BASE_PATH, 'output')

# Columns and data related information.
REDUNDANT_COLUMNS = ['begin_yearmonth', 'begin_day', 'end_yearmonth',
                     'end_day', 'year', 'month_name', 'end_time', ]

if __name__ == '__main__':
    ALL_PATHS = tuple(eval(x) for x in dir() if x.endswith('_PATH'))
    ALL_PATHS = tuple(os.path.abspath(x) for x in ALL_PATHS)
    PATHS_EXISTENCE = dict(zip(
        ALL_PATHS,
        map(os.path.exists, ALL_PATHS)))
    for k, v in PATHS_EXISTENCE.items():
        if v:
            pass
        else:
            raise OSError('Path \'{0}\' does not exist.'.format(k))
