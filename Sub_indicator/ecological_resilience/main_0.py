"""
Created on 2024-11-27

@author: Baoshi He


This script is used to calculate the first half of the ecological resilience formula.
"""



import numpy as np
from joblib import Parallel , delayed
from readAndWriteGeotif import *
from readGeotifWithBlock import *
from processBlockSize import *
from getArr2Blocks import *
from slidingWindow import *
from padEdgeAccordinSlidingWindow import *
from compositeImg import *
from convertNdarrayFromFloat2Int import *


if __name__ == '__main__':

    landuse_codes = [1 , 2 , 3  , 4 , 5 , 6 , 9]
    value_codes = [50 , 90 , 60 , 80 , 20 , 10 , 80]
    res = 30

    # year = 2000
    year = 2020

    tif  = r"E:\Desktop\中国滨海湿地数据集\中国滨海湿地_重分为一级类_cas{}_kar40_Albers.tif".format(year)
    im_width,im_height,im_bands,im_geotrans,im_proj = get_tif_information(tif)[:5]

    res = (30,30)

    ###########################################################################################################################
    window_num_list = [33 , 33]         # 1 km


    block_list = [10,10]
    block_size = process_block_size2((im_height , im_width) , block_list)

    row_pad = int((window_num_list[0] - 1) / 2)
    col_pad = int((window_num_list[1] - 1) / 2)


    ###########################################################################################################################
    block_list_joblib = [20 , 20]                                                              
    n_jobs = 30   
    jobs = block_list_joblib[0] * block_list_joblib[1] 
    batch_size = max(1 , (jobs + n_jobs - 1) // n_jobs)     

    sub_im_arrays = []

    with tqdm(total=block_list[0] * block_list[1] , desc="Processing", unit="iteration") as pbar:
        for row in range(0 , im_height , block_size[0]):       
            for col in range(0 , im_width , block_size[1]):  


                if (row == 0) and (col == 0):     
                    # block = arr[row : row + block_size[0] + row_pad , col : col + block_size[1] + col_pad]
                    x_offset = col
                    y_offset = row
                    x_size_subset = min(block_size[1] + col_pad , im_width - x_offset)            
                    y_size_subset = min(block_size[0] + row_pad , im_height - y_offset)
                    # block , nodatavalue = get_tif_subsetData(file_path = tif , x_offset = col, y_offset = row, x_size_subset = block_size[1] + col_pad, y_size_subset = block_size[0] + row_pad)
                    block , nodatavalue = get_tif_subsetData(file_path = tif , x_offset = x_offset, y_offset = y_offset, x_size_subset = x_size_subset, y_size_subset = y_size_subset)



                elif (row == 0) and (col != 0): 
                    # block = arr[row : row + block_size[0] + row_pad , col - col_pad : col + block_size[1] + col_pad]
                    x_offset = col - col_pad
                    y_offset = row
                    x_size_subset = min(block_size[1] + 2*col_pad , im_width - x_offset)           
                    y_size_subset = min(block_size[0] + row_pad , im_height - y_offset)
                    # block , nodatavalue = get_tif_subsetData(file_path = tif , x_offset = col - col_pad , y_offset = row , x_size_subset = block_size[1] + 2*col_pad, y_size_subset = block_size[0] + row_pad)
                    block , nodatavalue = get_tif_subsetData(file_path = tif , x_offset = x_offset, y_offset = y_offset, x_size_subset = x_size_subset, y_size_subset = y_size_subset)

                elif (row != 0) and (col == 0):
                    # block = arr[row - row_pad : row + block_size[0] + row_pad  , col : col + block_size[1] + col_pad]
                    x_offset = col
                    y_offset = row - row_pad
                    x_size_subset = min(block_size[1] + col_pad , im_width - x_offset)                
                    y_size_subset = min(block_size[0] + 2*row_pad , im_height - y_offset)
                    # block , nodatavalue = get_tif_subsetData(file_path = tif , x_offset = col , y_offset = row - row_pad , x_size_subset = block_size[1] + col_pad, y_size_subset = block_size[0] + 2*row_pad)
                    block , nodatavalue = get_tif_subsetData(file_path = tif , x_offset = x_offset, y_offset = y_offset, x_size_subset = x_size_subset, y_size_subset = y_size_subset)

                elif (row != 0) and (col !=0 ): 
                    # block = arr[row - row_pad : row + block_size[0] + row_pad  , col - col_pad: col + block_size[1] + col_pad]
                    x_offset = col - col_pad
                    y_offset = row - row_pad
                    x_size_subset = min(block_size[1] + 2*col_pad , im_width - x_offset)             
                    y_size_subset = min(block_size[0] + 2*row_pad , im_height - y_offset)
                    # block , nodatavalue = get_tif_subsetData(file_path = tif , x_offset = col - col_pad , y_offset = row - row_pad , x_size_subset = block_size[1] + 2*col_pad, y_size_subset = block_size[0] + 2*row_pad)
                    block , nodatavalue = get_tif_subsetData(file_path = tif , x_offset = x_offset, y_offset = y_offset, x_size_subset = x_size_subset, y_size_subset = y_size_subset)


                # print("block:", block)

                block = block.astype(float)
                block[block == nodatavalue] = np.nan


                blocks = get_arr2_blocks(arr = block , window_num_list = window_num_list , block_list = block_list_joblib)

                # multiprocessing
                sub_im_arrays_blocks = Parallel(n_jobs = n_jobs , batch_size = batch_size)(delayed(sliding_window)(sub_arr , window_num_list , landuse_codes , value_codes , res) for sub_arr in blocks)

                sub_im_arrays.append(sub_im_arrays_blocks)

                pbar.update(1)

    print("分块中的joblib处理完毕，开始拼装数据......................")



    all_min_values = []  
    all_max_values = [] 


    for i in range(len(sub_im_arrays)):
        for j in sub_im_arrays[i]:
            min_val = np.nanmin(j)
            max_val = np.nanmax(j)
            # print(min_val , max_val)

            if not np.isnan(min_val):
                all_min_values.append(min_val)
            if not np.isnan(max_val):
                all_max_values.append(max_val)       


    overall_min = np.nanmin(all_min_values)
    overall_max = np.nanmax(all_max_values)


    print("Overall minimum value:", overall_min)
    print("Overall maximum value:", overall_max)


    convert_type = np.uint32

    setNodataValue = np.iinfo(convert_type).max   

    convert_arr_from_float2int(sub_im_arrays , enlargement_factor = 1 , convert_type = convert_type)


    for index , arr_list in enumerate(sub_im_arrays):
        sub_im_arrays[index] = composite_img_shannon_index_block(arr_list , block_list_joblib)


    final_data = composite_img_shannon_index_block(arr_list = sub_im_arrays , block_list_joblib = block_list)

    final_data = pad_edge_according_windows(final_data , window_num_list  , number = setNodataValue)

    print("final_data:" , final_data)            
    print("fianl_data.shape:" , final_data.shape)


    # output tif
    ####################################################################################################################
    name = r"E:\Desktop\中国滨海湿地数据集\output\中国滨海湿地_生态弹性限度0_{}.tif".format(year)
    mat = final_data
    array_to_tif2(name , mat , im_geotrans ,im_proj , nodata_value = setNodataValue)
    print(f"{name} -----------------> successed！")


