"""
Created on 2024-11-27

@author: Baoshi He


This program is used to calculate the CEQI value.
"""


import numpy as np
from readAndWriteGeotif import *



structure = 0.25
structure_son = 0.25
course = 0.25
course_son = 0.333
function = 0.25
function_son = 0.5
restore = 0.25


folder_names = ["BSSI" , "cohesion指数" , "division指数" , "LST" , "SPWI" , "斑块密度" , "景观多样性" , "生境质量" , "生态弹性限度" , "碳密度"]
weights = [course * course_son , structure * structure_son , structure * structure_son , course * course_son , course * course_son , structure * structure_son , structure * structure_son , function * function_son , restore , function * function_son]


# year = 2000
year = 2020


eco_im_data = None


idx_tif_paths = [r"H:\中国滨海湿地生态质量评估\最终归一化结果\BSSI\{}_BSSI_湿地范围掩膜_归一化.tif".format(year) , 
            r"H:\中国滨海湿地生态质量评估\最终归一化结果\cohesion指数\中国滨海湿地景观cohesion指数{}_9窗口_湿地范围掩膜_归一化.tif".format(year) , 
            r"H:\中国滨海湿地生态质量评估\最终归一化结果\division指数\中国滨海湿地景观division指数{}_9窗口_湿地范围掩膜_归一化.tif".format(year) , 
            r"H:\中国滨海湿地生态质量评估\最终归一化结果\LST\LST_{}_湿地范围掩膜_归一化.tif".format(year) , 
            r"H:\中国滨海湿地生态质量评估\最终归一化结果\SPWI\SPWI_{}_修正_湿地范围掩膜_归一化.tif".format(year) , 
            r"H:\中国滨海湿地生态质量评估\最终归一化结果\斑块密度\中国滨海湿地景观斑块密度_{}_9窗口_湿地范围掩膜_归一化.tif".format(year) , 
            r"H:\中国滨海湿地生态质量评估\最终归一化结果\景观多样性\中国滨海湿地景观多样性指数{}_9窗口_湿地范围掩膜_归一化.tif".format(year) , 
            r"H:\中国滨海湿地生态质量评估\最终归一化结果\生境质量\quality{}_c_湿地范围掩膜_归一化.tif".format(year) , 
            r"H:\中国滨海湿地生态质量评估\最终归一化结果\生态弹性限度\中国滨海湿地生态弹性限度_{}_9窗口_湿地范围掩膜_归一化.tif".format(year) , 
            r"H:\中国滨海湿地生态质量评估\最终归一化结果\碳密度\中国滨海湿地总碳密度_{}_湿地范围掩膜_归一化.tif".format(year)]

for tif in idx_tif_paths:
    # search weight
    folder_name = tif.rsplit("\\" , 2)[1]
    idx = folder_names.index(folder_name)
    weight = weights[idx]
    # print(folder_name , weight)
    
    # break


    im_width,im_height,im_bands,im_geotrans,im_proj,im_data , nodatavalue = get_tif_information(file_path = tif)
    
    im_data = im_data.astype(np.float32)
    im_data[im_data == nodatavalue] = np.nan

    im_data = im_data * weight

    if eco_im_data is None:
        eco_im_data = im_data
    
    else:
        eco_im_data += im_data

    del im_data



eco_im_data[np.isnan(eco_im_data)] = 2

##############################################################################################
name = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\最终评估结果\中国滨海湿地生态质量综合评估_{}".format(year)

array_to_tif2(name = name , mat = eco_im_data , im_geotrans = im_geotrans ,im_proj = im_proj , nodata_value = 2)
print(f"{name} ----------------------------------------------------> successfully!")




































