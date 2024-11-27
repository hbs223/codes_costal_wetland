"""
Created on 2024-11-27

@author: Baoshi He


This program is intended to compute the maximum and minimum values of each indicator from the 2000 and 2020 TIFF data, and write the results to an Excel file for subsequent TIFF normalization.
"""



from normalize import *
import numpy as np
from readAndWriteGeotif import *
import os
import numpy.ma as ma
import pandas as pd



folder_names = ["BSSI" , "cohesion指数" , "division指数" , "LST" , "SPWI" , "斑块密度" , "景观多样性" , "生境质量" , "生态弹性限度" , "碳密度"]
directions = ["negetive" , "positive" , "negetive" , "negetive" , "positive" , "negetive" , "positive" , "positive" , "positive" , "positive"]
df = pd.DataFrame(index = folder_names , columns = ["max_value", "min_value"])


father_folder = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\用于归一化的原始数据掩膜结果"
output_father_folder = r"H:\中国滨海湿地生态质量评估\最终归一化结果"

for folder_name , direction in zip(folder_names , directions):

    floder_path = os.path.join(father_folder , folder_name)
    # print(floder_path)

    tifs = get_file_path(floder_path = floder_path , suffix = ".tif")

    print("待处理tif路径:" , tifs)

    if len(tifs) == 2:

        im_width,im_height,im_bands,im_geotrans,im_proj,im_data_2000 , nodatavalue_2000 = get_tif_information(tifs[0])
        im_width,im_height,im_bands,im_geotrans,im_proj,im_data_2020 , nodatavalue_2020 = get_tif_information(tifs[1])


        mask_2000 = im_data_2000 == nodatavalue_2000
        mask_2020 = im_data_2020 == nodatavalue_2020


        masked_im_data_2000 = ma.masked_array(data = im_data_2000 , mask = mask_2000)
        masked_im_data_2020 = ma.masked_array(data = im_data_2020 , mask = mask_2020)

        max_2000 = masked_im_data_2000.max()
        min_2000 = masked_im_data_2000.min()
        max_2020 = masked_im_data_2020.max()
        min_2020 = masked_im_data_2020.min()

        if max_2000 >= max_2020:
            max_value = max_2000
        else:
            max_value = max_2020

        if min_2000 <= min_2020:
            min_value = min_2000
        else:
            min_value = min_2020

        print(max_value , min_value)
       
        df.loc[folder_name]["max_value"] = max_value
        df.loc[folder_name]["min_value"] = min_value


        del im_data_2000 , im_data_2020 , masked_im_data_2000 , masked_im_data_2020

df_name = r"E:\Desktop\Python改变地球\A中国滨海湿地处理\指标归一化\所有指标的最大最小值.xlsx"
df.to_excel(df_name)
print(f"{df_name} --------------------> successfully!")




































