"""
Created on 2024-11-27

@author: Baoshi He


Set the no data values of the calculated CEQI data to 0.
"""

from readAndWriteGeotif import *
import numpy as np
# import numpy.ma as ma


costal_area = r"E:\Desktop\Python改变地球\A中国滨海湿地生态质量评估\湿地范围\output\20002020中国滨海湿地区域.tif"
im_width,im_height,im_bands,im_geotrans,im_proj, im_data_costal_area , nodatavalue_costal_area = get_tif_information(file_path = costal_area)
# print(im_data_costal_area)


mask = ~(im_data_costal_area == nodatavalue_costal_area)
# print(mask)

years = [2000 , 2020]


for year in years:

    eco = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\最终评估结果\中国滨海湿地生态质量综合评估_v2_{}.tif".format(year)
    im_width,im_height,im_bands,im_geotrans,im_proj, im_data_eco , nodatavalue_eco = get_tif_information(file_path = eco)
    print(im_data_eco)
    eco_area = (im_data_eco == nodatavalue_eco)
    print(eco_area)
    set0_bool = (mask & eco_area)
    print(set0_bool)
    # break
    im_data_eco[set0_bool] = 0

    ##############################################################################################
    name = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\最终评估结果\中国滨海湿地生态质量综合评估_非背景区域非湿地设置为0_{}".format(year)

    array_to_tif2(name = name , mat = im_data_eco , im_geotrans = im_geotrans ,im_proj = im_proj , nodata_value = nodatavalue_eco)
    print(f"{name} ----------------------------------------------------> successfully!")








































