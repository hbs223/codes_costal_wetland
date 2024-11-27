"""
Created on 2024-11-27

@author: Baoshi He


Calculate the difference in CEQI values between 2020 and 2000.
"""

from readAndWriteGeotif import *
import numpy as np



eco_2000 = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\最终评估结果\中国滨海湿地生态质量综合评估_非背景区域非湿地设置为0_2000.tif"
eco_2020 = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\最终评估结果\中国滨海湿地生态质量综合评估_非背景区域非湿地设置为0_2020.tif"



im_width,im_height,im_bands,im_geotrans,im_proj,im_data_2020 , nodatavalue_2020 = get_tif_information(file_path = eco_2020)
im_width,im_height,im_bands,im_geotrans,im_proj,im_data_2000 , nodatavalue_2000 = get_tif_information(file_path = eco_2000)


im_data_2020 = im_data_2020.astype(np.float32)
im_data_2020[im_data_2020 == nodatavalue_2020] = np.nan

im_data_2000 = im_data_2000.astype(np.float32)
im_data_2000[im_data_2000 == nodatavalue_2000] = np.nan

final_eco_im_data = im_data_2020 - im_data_2000

final_eco_im_data[np.isnan(final_eco_im_data)] = 2

##############################################################################################
name = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\最终评估结果\中国滨海湿地生态质量综合评估_20002020_差值_v2_python计算结果"

array_to_tif2(name = name , mat = final_eco_im_data , im_geotrans = im_geotrans ,im_proj = im_proj , nodata_value = 2)
print(f"{name} ----------------------------------------------------> successfully!")

