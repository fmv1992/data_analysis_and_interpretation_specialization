"""
Created on Sat May 14 12:24:08 2016

Author: Felipe M. Vieira

Description:

Cuts the database to contain only the following variables:

"""

import os

import numpy as np
import pandas as pd  # version '0.17.0'
import pandas_utilities  # for cosmetic adjustments and data standardization

from project_library import DATASETS_PATH


def compress_dataset():
    db = pd.read_csv(
        os.path.join(
            DATASETS_PATH,
            'wdi_data_all_time_utf8_encoded.csv'),
        index_col=0)
    # sha1sum of the original file; deleted to be uploaded to github
    # 2e8ad6da7f8a65633f0debdfc532b4923fb0514c
    # wdi_data_all_time_utf8_encoded.csv

    out_path = os.path.join(
        DATASETS_PATH, 'wdi_data_all_time_utf8_encoded_and_compressed.csv.gz')
    db.to_csv(out_path, compression='gzip')


if __name__ == '__main__':
    compress_dataset()
