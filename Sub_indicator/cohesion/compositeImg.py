import numpy as np


def composite_img(arr_list , block_list_joblib):
    
    composite_img_list = []
    for row in range(block_list_joblib[0]):
        
        row_list = []
        for col in range(block_list_joblib[1]):
            idx = row * block_list_joblib[1] + col
            block_data = arr_list[idx]

            row_list.append(block_data)
        
        row_list_arr = np.concatenate(row_list , axis = 1)

        composite_img_list.append(row_list_arr)
    
    result_arr = np.concatenate(composite_img_list , axis = 0)

    return result_arr


def composite_img_shannon_index_block(arr_list , block_list_joblib):

    row_data_list = []    
    for row in range(block_list_joblib[0]):

        row_list = []
        for col in range(block_list_joblib[1]):
            idx= row * block_list_joblib[1] + col
            block_result = arr_list[idx]

            if block_result.size != 0:   
                row_list.append(block_result)

        
        if len(row_list) != 0:      
            row_data = np.concatenate(row_list , axis=1)
            row_data_list.append(row_data)

    if len(row_data_list) != 0:  

        final_data = np.concatenate(row_data_list , axis = 0)

    else:
        final_data = np.empty((0, 0) , dtype=int)
    return final_data













