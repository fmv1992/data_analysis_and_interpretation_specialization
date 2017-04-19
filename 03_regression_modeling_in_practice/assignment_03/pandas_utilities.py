# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 07:37:20 2016

Author: Felipe Vieira
"""
import pandas as pd
import string

universe_of_digits = string.ascii_lowercase + string.digits + '_'

def clean_string(s):
    """Takes s as str input and makes it a standard lowercase with '_' as
    separator."""
    s = str(s).lower().replace(' ', '_')
    return ''.join(filter(lambda x: x in universe_of_digits, s))
    

def clean_dataframe(df):
    """Cleans the dataframe."""
    df.rename(columns=clean_string, inplace=True)
    return None