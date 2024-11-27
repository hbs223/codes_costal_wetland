import numpy as np
from scipy import ndimage
from cmodule.compute_division import compute_division



def custom_operation(neighborhood_array , window_num_list):

    if np.isnan(neighborhood_array).any():
        return np.nan 
    else:

        neighborhood_array = neighborhood_array.reshape(window_num_list[0] , window_num_list[1]).astype(np.int32)

        diviosn = compute_division(neighborhood_array)

        return diviosn

























