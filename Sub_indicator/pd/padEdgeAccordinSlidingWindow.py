import numpy as np


def pad_edge_according_windows(arr , window_num_list  , number = "nan"):


    pad_row = int((window_num_list[0] - 1) / 2)     
    pad_col = int((window_num_list[1] - 1) / 2)   

    if number == "nan":
        arr = arr.astype(float)
        arr_pad = np.pad(arr , pad_width = ((int(pad_row),int(pad_row)) , (int(pad_col),int(pad_col))) , mode = "constant" , constant_values = (np.nan , np.nan))
    else:
        arr_pad = np.pad(arr , pad_width = ((int(pad_row),int(pad_row)) , (int(pad_col),int(pad_col))) , mode = "constant" , constant_values = (number , number))

    return arr_pad