import numpy as np



def process_block_size(array , block_list):

    block_row = block_list[0]
    block_col = block_list[1]
    
    block_size_row = int(array.shape[0] / block_row) + 1
    block_size_col = int(array.shape[1] / block_col) + 1
    block_size = (block_size_row , block_size_col)

    return block_size


def process_block_size2(arr_shape , block_list):

    block_row = block_list[0]
    block_col = block_list[1]
    
    block_size_row = int(arr_shape[0] / block_row) + 1
    block_size_col = int(arr_shape[1] / block_col) + 1
    block_size = (block_size_row , block_size_col)

    return block_size