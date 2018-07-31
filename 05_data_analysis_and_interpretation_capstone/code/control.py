"""Control file for Capstone project.

Contains the constants and important variables for this assignment.

Coursera Course: Data Analysis and Interpretation Capstone.

    https://www.coursera.org/learn/data-analysis-capstone

This course is one in a series of: Data Analysis and Interpretation

Assignment: Capstone.
"""
import os

# os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Path variables.
BASE_PATH = os.path.dirname(
    os.path.abspath(
        os.path.dirname(
            __file__)))
DATA_PATH = os.path.join(BASE_PATH, 'data')
ZIP_PATH = os.path.join(DATA_PATH, 'storm_event_data.zip')
OUTPUT_PATH = os.path.join(BASE_PATH, 'output')

# Columns and data related information.
REDUNDANT_COLUMNS = ['begin_yearmonth', 'begin_day', 'end_yearmonth',
                     'end_day', 'year', 'month_name', 'end_time', 'begin_time']
RELEVANT_COLUMNS = ['injuries_direct', 'injuries_indirect', 'deaths_direct',
                    'deaths_indirect', 'damage_property', 'damage_crops', ]
DAMAGE_COLUMNS = ['damage_property', 'damage_crops', ]

RENAME_COLUMNS = {
    'magnitude': 'magnitude_of_wind_speeds_or_hail_size',
}


FEET_TO_M = .3048
MILES_TO_M = 1609


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
