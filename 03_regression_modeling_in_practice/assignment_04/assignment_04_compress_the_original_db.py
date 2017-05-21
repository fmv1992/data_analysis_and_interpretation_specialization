# -*- coding: utf-8 -*-
"""
Created on Sat May 14 12:24:08 2016

Author: Felipe M. Vieira

Description:

Cuts the database to contain only the following variables:

"""
import numpy as np
import pandas as pd  # version '0.17.0'
import pandas_utilities  # for cosmetic adjustments and data standardization

db = pd.read_csv('wdi_data_all_time_utf8_encoded.csv', index_col=0)
# sha1sum of the original file; deleted to be uploaded to github
# 2e8ad6da7f8a65633f0debdfc532b4923fb0514c  wdi_data_all_time_utf8_encoded.csv


db.to_csv('wdi_data_all_time_utf8_encoded_and_compressed.csv', compression='gzip')