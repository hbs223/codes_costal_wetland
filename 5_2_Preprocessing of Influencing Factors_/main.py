"""
Created on 2024-11-27

@author: Baoshi He


Calculate the TIFF data of the difference in all influencing factor values between 2020 and 2000.
"""


from readAndWriteGeotif import *
import numpy as np
import os
import dask.array as da


########################################################################
father_fea = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\影响因素_行列号对齐"
########################################################################
output_folder = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\影响因素_行列号对齐_相减"
feas_name = os.listdir(father_fea)

# print(feas)

for fea_name in feas_name:

    fea_folder_path = os.path.join(father_fea , fea_name)

    tifs = get_file_path(floder_path = fea_folder_path , suffix = ".tif")
    print(tifs)
    im_width,im_height,im_bands,im_geotrans,im_proj,im_data_2000 , nodatavalue_2000 = get_tif_information(file_path = tifs[0])
    im_width,im_height,im_bands,im_geotrans,im_proj,im_data_2020 , nodatavalue_2020 = get_tif_information(file_path = tifs[1])

    

    im_data_2020 = im_data_2020.astype(np.float32)
    im_data_2020[im_data_2020 == nodatavalue_2020] = np.nan

    dasked_im_data_2020 = da.from_array(im_data_2020 , chunks = (1000 , 1000))
    del im_data_2020 , nodatavalue_2020

    im_data_2000 = im_data_2000.astype(np.float32)
    im_data_2000[im_data_2000 == nodatavalue_2000] = np.nan

    dasked_im_data_2000 = da.from_array(im_data_2000 , chunks = (1000 , 1000))
    del im_data_2000 , nodatavalue_2000
    

    change_im_data = (dasked_im_data_2020 - dasked_im_data_2000).compute()


    ##############################################################################################
    file_name = f"{fea_name}_相减_2020_2000"
    name = os.path.join(os.path.join(output_folder , fea_name) , file_name)

    array_to_tif(name = name , mat = change_im_data , im_geotrans = im_geotrans ,im_proj = im_proj)
    print(f"{name} ----------------------------------------------------> successfully!")















