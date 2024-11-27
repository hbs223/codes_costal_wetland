from processBlockSize import *



def get_arr2_blocks(arr , window_num_list , block_list = [1 , 1]):


    block_size = process_block_size(arr , block_list)


    row_pad = int((window_num_list[0] - 1) / 2)
    col_pad = int((window_num_list[1] - 1) / 2)


    blocks = []


    for row in range(0 , arr.shape[0] , block_size[0]):
        for col in range(0 , arr.shape[1] , block_size[1]):
            if (row == 0) and (col == 0):      
                block = arr[row : row + block_size[0] + row_pad , col : col + block_size[1] + col_pad]

            elif (row == 0) and (col != 0):  
                block = arr[row : row + block_size[0] + row_pad , col - col_pad : col + block_size[1] + col_pad]

            elif (row != 0) and (col == 0):  
                block = arr[row - row_pad : row + block_size[0] + row_pad  , col : col + block_size[1] + col_pad]

            elif (row != 0) and (col !=0 ):  
                block = arr[row - row_pad : row + block_size[0] + row_pad  , col - col_pad: col + block_size[1] + col_pad]

            blocks.append(block)
            # print("block:", block)

    return blocks  