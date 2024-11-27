"""
Created on 2024-11-27

@author: Baoshi He


Remove the samples from 𝑋 where any value is NaN.
"""

from readAndWriteGeotif import *
import numpy as np
from delNanRowOrCol import *


npys = ['E:\\Desktop\\Python改变地球\\A中国滨海湿地处理\\9_写出干净的采样数据\\arrOutput\\中国滨海湿地GDP_相减_20202000.npy', 
 'E:\\Desktop\\Python改变地球\\A中国滨海湿地处理\\9_写出干净的采样数据\\arrOutput\\中国滨海湿地NDVI_相减_20202000.npy', 
 'E:\\Desktop\\Python改变地球\\A中国滨海湿地处理\\9_写出干净的采样数据\\arrOutput\\中国滨海湿地PET_相减_20202000.npy', 
 'E:\\Desktop\\Python改变地球\\A中国滨海湿地处理\\9_写出干净的采样数据\\arrOutput\\中国滨海湿地POP_相减_20202000.npy', 
 'E:\\Desktop\\Python改变地球\\A中国滨海湿地处理\\9_写出干净的采样数据\\arrOutput\\中国滨海湿地tmp_相减_20202000.npy', 
 'E:\\Desktop\\Python改变地球\\A中国滨海湿地处理\\9_写出干净的采样数据\\arrOutput\\中国滨海湿地建成区_相减_20202000.npy',
 'E:\\Desktop\\Python改变地球\\A中国滨海湿地处理\\9_写出干净的采样数据\\arrOutput\\中国滨海湿地降雨_相减_20202000.npy', 
 'E:\\Desktop\\Python改变地球\\A中国滨海湿地处理\\9_写出干净的采样数据\\arrOutput\\中国滨海湿地生态质量综合评估_20002020_差值_v2_python计算结果.npy', 
 'E:\\Desktop\\Python改变地球\\A中国滨海湿地处理\\9_写出干净的采样数据\\arrOutput\\中国滨海湿地土地利用变化_2020扩大100倍_20202000.npy'
 ]
print(npys)


xs = None

for npy in npys:
    x = np.load(npy)
    if xs is None:
        xs = x
    else:
        xs = np.hstack((xs , x[: , -1].reshape(-1 , 1)))


    print(f'{npy} ---------------------------->> 处理完毕！')

data_name_withNan = r"E:\Desktop\Python改变地球\A中国滨海湿地处理\9_写出干净的采样数据\arrOutput\中国滨海湿地生态质量及影响因素_包含nan的.npy"
np.save(file = data_name_withNan , arr = xs)
print(f"{data_name_withNan} --------------------------------> successfully saved!!!")


# Delete the samples with NaN values.
data_cleaned = delete_nan_RowsOrColumns(array = xs , axis = 1)

data_cleaned_name = r"E:\Desktop\Python改变地球\A中国滨海湿地处理\9_写出干净的采样数据\finalDataArr\中国滨海湿地最终无nan样本.npy"
np.save(data_cleaned_name , data_cleaned)
print(f"{data_cleaned_name} --------------------> successfully!")















