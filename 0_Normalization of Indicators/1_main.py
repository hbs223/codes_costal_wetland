"""
Created on 2024-11-27

@author: Baoshi He


This program is designed to calculate the normalized TIFF data for each indicator for the years 2000 and 2020.
"""


from normalize import *
import numpy as np
from readAndWriteGeotif import *
import os
import numpy.ma as ma
import pandas as pd
import dask.array as da


df = pd.read_excel(r"E:\Desktop\Python改变地球\A中国滨海湿地处理\指标归一化\所有指标的最大最小值.xlsx" , index_col = 0)
print(df)

# folder_names = ["BSSI" , "cohesion指数" , "division指数" , "LST" , "SPWI" , "斑块密度" , "景观多样性" , "生境质量" , "生态弹性限度" , "碳密度"]
# directions = ["negetive" , "positive" , "negetive" , "negetive" , "positive" , "negetive" , "positive" , "positive" , "positive" , "positive"]

folder_names = ["cohesion指数" , "division指数" , "LST" , "SPWI" , "斑块密度" , "景观多样性" , "生境质量" , "生态弹性限度" , "碳密度"]
directions = ["positive" , "negetive" , "negetive" , "positive" , "negetive" , "positive" , "positive" , "positive" , "positive"]



father_folder = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\用于归一化的原始数据掩膜结果"
output_father_folder = r"H:\中国滨海湿地生态质量评估\最终归一化结果"


for folder_name , direction in zip(folder_names , directions):

    floder_path = os.path.join(father_folder , folder_name)
    # print(floder_path)

    tifs = get_file_path(floder_path = floder_path , suffix = ".tif")

    print("待处理tif路径:" , tifs)

    max_value = df.loc[folder_name]["max_value"]
    min_value = df.loc[folder_name]["min_value"]
    print(max_value, min_value)  

    for tif in tifs:
        im_width,im_height,im_bands,im_geotrans,im_proj,im_data , nodatavalue = get_tif_information(tif)

        dask_im_data = da.from_array(im_data , chunks = (1000 , 1000))
        del im_data
        mask = dask_im_data == nodatavalue


        dask_masked_im_data = da.ma.masked_equal(dask_im_data , nodatavalue)
        del dask_im_data
        normalized_dask_masked_im_data = normalize(max_value = max_value, min_value = min_value , year_arr = dask_masked_im_data , direction = direction)
        del dask_masked_im_data


        normalized_dask_im_data = da.where(mask, 2 , normalized_dask_masked_im_data)
        del normalized_dask_masked_im_data
        del mask


        normalized_dask_im_data = normalized_dask_im_data.compute()


        # output tif
        output_folder = os.path.join(output_father_folder , folder_name)
        fileName = os.path.basename(tif).rsplit("." , 1)[0] + "_归一化"

        output_file = os.path.join(output_folder , fileName)

        array_to_tif2(name = output_file , mat = normalized_dask_im_data , im_geotrans = im_geotrans , im_proj = im_proj , nodata_value = 2)
        print(f"{output_file} ------------------> successfully!")

        del normalized_dask_im_data










































