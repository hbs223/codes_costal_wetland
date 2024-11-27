import numpy as np
# from scipy.stats import entropy
from numba import njit  


@njit(nogil = True)
def calc_with_jit(Pks):
    shannon_index = 0
    for i in range(len(Pks)):
        rate = -1 * Pks[i] * np.log(Pks[i])    

        shannon_index += rate 

    return shannon_index


def custom_operation(neighborhood_array):
    print("this is a easy test!")
    if np.isnan(neighborhood_array).any():
        return np.nan             
    else:

        flattened_arr = neighborhood_array.flatten()

        counts = np.unique(flattened_arr, return_counts=True)[1]

        Pks = counts / counts.sum()    

        shannon_index = calc_with_jit(Pks)

        return shannon_index
    


