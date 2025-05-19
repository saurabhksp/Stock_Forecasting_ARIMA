# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Data Processing: Help Functions
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

import numpy as np
from pathlib import Path
from scipy.io import loadmat  # this is the SciPy module that loads mat-files
import matplotlib.pyplot as plt
from datetime import datetime, date, time
import pandas as pd

"""
    Load a mat-file with scipy.io
"""
def load_mat_file(filepath):
    mat = loadmat(filepath)  # load mat-file
    return mat

"""
    Convert mat-file to pandas
"""
def convert_mat_to_pandas(mat):
    df = pd.DataFrame(mat)
    return df

"""
    compute extrema from positions px, py
"""
def compute_extrema_2D(dataset):
    xmin=np.min(dataset['px'])
    xmax=np.max(dataset['px'])
    ymin = np.min(dataset['py'])
    ymax = np.max(dataset['py'])
    return xmin, xmax, ymin, ymax

"""
    get path one level above
"""
def get_superior_path():
        return Path(__file__).parent

"""
    get a bool array of a pandas dataset depending on the values of a specific column
"""
def get_bool_array_depending_on_column_value(df, column, value):
    new_df=df[column]==value
    return new_df

"""
    get a new pandas dataframe depending on a boolean array
"""
def selection_of_dataset_by_boolean_array(df, bool_rows):
    sel_df=df[bool_rows]
    return sel_df

'''
   Get selection of dataset specified by a column and the range from min_val to max_val
   Example: the dataset should be selected by the time range from [4s, 6s]
'''
def dataset_by_range(df, column, min_val, max_val):
    a = df[column] >= min_val
    b = df[column] <= max_val
    c = a & b
    new_df=selection_of_dataset_by_boolean_array(df, c)
    return new_df