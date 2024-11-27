"""
Created on 2024-11-27

@author: Baoshi He


Remove rows or columns containing NaN values from the 2D data.
"""


import numpy as np



def delete_nan_RowsOrColumns(array , axis = 1):


    if axis == 0:      # Remove columns that contain NaN values.

        nan_columns = np.isnan(array).any(axis = 0)

        data_cleaned = array[:, ~nan_columns]

        return data_cleaned

    elif axis == 1:       # Remove rows that contain NaN values in any column.
        nan_rows = np.isnan(array).any(axis = 1)

        data_cleaned = array[~nan_rows , :]

        return data_cleaned

    else:
        print("请输入正确的轴号")