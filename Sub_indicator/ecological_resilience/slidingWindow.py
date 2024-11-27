from slidingWindowFunction import *



def sliding_window(arr , window_num_list, landuse_codes , value_codes , res):


    if (arr.shape[0] >= window_num_list[0]) and (arr.shape[1] >= window_num_list[1]):

        window_view = np.lib.stride_tricks.sliding_window_view(arr, window_shape = (window_num_list[0] , window_num_list[1]))
        
        window_view = window_view.reshape((window_view.shape[0],window_view.shape[1],window_view.shape[2] * window_view.shape[3]))

        window_view = np.transpose(window_view ,  (2,0,1))

        shannon_index_2D = np.apply_along_axis(custom_operation_ecological_limit , axis = 0 , arr = window_view , landuse_codes = landuse_codes , value_codes = value_codes , res = res)

    else:

        shannon_index_2D = np.empty((0, 0) , dtype=int)
        
    
    return shannon_index_2D 