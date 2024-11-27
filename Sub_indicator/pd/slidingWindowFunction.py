import numpy as np
# from scipy.stats import entropy
from numba import njit  
import pylandstats as pls



# @njit(nogil = True)
def custom_operation(neighborhood_array , window_num_list , res):
    if np.isnan(neighborhood_array).any():
        return np.nan                   
    else:
        neighborhood_array = neighborhood_array.reshape(window_num_list[0] , window_num_list[1])           
        pd = pls.Landscape(neighborhood_array , res = res).patch_density()
        
        return pd
    






















