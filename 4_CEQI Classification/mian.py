"""
Created on 2024-11-27

@author: Baoshi He


Classify the CEQI difference between 2020 and 2000.
"""

from readAndWriteGeotif import *
import numpy as np
import numpy.ma as ma



change_path = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\最终评估结果\中国滨海湿地生态质量综合评估_20002020_差值_v2_python计算结果.tif"


im_width,im_height,im_bands,im_geotrans,im_proj,im_data , nodatavalue = get_tif_information(file_path = change_path)

print(im_data)

im_data = im_data.astype(np.float32)
im_data[im_data == nodatavalue] = np.nan


##############################################################################################
reclassified_arr = np.full_like(im_data, np.nan)

# The classification criteria are based on the natural breaks algorithm in ArcGIS Pro.
con_bool_min3 = (im_data <= -0.516824)
reclassified_arr[con_bool_min3] = -3
del con_bool_min3

con_bool_min2 = (im_data <= -0.256918) & (im_data > -0.516824)
reclassified_arr[con_bool_min2] = -2
del con_bool_min2

con_bool_min1 = (im_data <= -0.05) & (im_data > -0.256918)
reclassified_arr[con_bool_min1] = -1
del con_bool_min1

con_bool_0 = (im_data <= 0.05) & (im_data > -0.05)
reclassified_arr[con_bool_0] = 0
del con_bool_0

con_bool_1 = (im_data <= 0.232217) & (im_data > 0.05)
reclassified_arr[con_bool_1] = 1
del con_bool_1

con_bool_2 = (im_data <= 0.481635) & (im_data > 0.232217)
reclassified_arr[con_bool_2] = 2
del con_bool_2

con_bool_3 = im_data > 0.481635
reclassified_arr[con_bool_3] = 3
del con_bool_3

info = np.iinfo(np.int16)

reclassified_arr[np.isnan(reclassified_arr)] = info.max  # 127

reclassified_arr = reclassified_arr.astype(np.int16)

##############################################################################################
name = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\最终评估结果\中国滨海湿地生态质量综合评估_20002020_差值_v2_python计算结果_重分成7类结果_带0的_零点零五"

array_to_tif2(name = name , mat = reclassified_arr , im_geotrans = im_geotrans ,im_proj = im_proj , nodata_value = info.max)
print(f"{name} ----------------------------------------------------> successfully!")












