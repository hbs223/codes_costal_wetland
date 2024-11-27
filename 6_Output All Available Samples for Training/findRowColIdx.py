"""
Created on 2024-11-27

@author: Baoshi He


Find the row and column indices of non-NaN values in the array.
"""


import numpy as np



def he_findNumIndex(array , num = "nan"):

    if num == "nan":
        non_nan_indices = np.argwhere(~np.isnan(array))

    else:
        non_nan_indices = np.argwhere(~(array == num))
        
    return non_nan_indices


def he_findValueAccordingIdx(idx , array , idx_row = 0 , idx_col = 1):


    add_colNum = idx.shape[1] + 1
    result = np.empty((idx.shape[0], add_colNum)) 

    for i in range(idx.shape[1]):

        result[:, i] = idx[:, i]

    result[:, -1] = array[idx[:, idx_row].astype(int), idx[:, idx_col].astype(int)]

    return result










