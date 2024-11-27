import numpy as np
# from scipy.stats import entropy
from numba import jit, njit



@jit(nopython=True , nogil=True)
def ecological_limit(value , landuse_codes , value_codes , res):
    eco = 0
    value_size = len(value)

    for i, score in zip(landuse_codes , value_codes):
        count_i = 0
        for j in range(value_size):
            if value[j] == i:
                count_i += 1

        eco_sec = (count_i * res * res) * score
        eco += eco_sec

    return eco


def custom_operation_ecological_limit(neighborhood_array , landuse_codes , value_codes , res):

    if np.isnan(neighborhood_array).any():
        return np.nan
    else:
        value = neighborhood_array.flatten()

        eco = ecological_limit(value , landuse_codes , value_codes , res)

        return float(eco)
