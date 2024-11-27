"""
Created on 2024-11-27

@author: Baoshi He


Obtain all pixel samples that can be used for machine learning training.
"""




from readAndWriteGeotif import *
import numpy as np
from findRowColIdx import *
from delNanRowOrCol import *
import os


tifs_path = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\影响因素_行列号对齐_相减"

tifs = get_file_path(floder_path = tifs_path , suffix = ".tif")

tifs.append(r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\最终评估结果\中国滨海湿地生态质量综合评估_20002020_差值_v2_python计算结果")
print("Xs and y(float):" , tifs)


y_folder = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\最终评估结果\中国滨海湿地生态质量综合评估_20002020_差值_v2_python计算结果_重分成7类结果_带0的_零点零五.tif"

y_feature , y_nodatavalue = get_tif_information(y_folder)[-2:]
y_feature = y_feature.astype(float)
y_feature[y_feature == y_nodatavalue] = np.nan

non_nan_indices = he_findNumIndex(y_feature , num = "nan")

print("non_nan_indices:" , non_nan_indices)


# Based on the row and column indices where y is not NaN, identify all the non-NaN values in y.
result = he_findValueAccordingIdx(non_nan_indices , y_feature , idx_row = 0 , idx_col = 1)
del y_feature



# Check if the row and column indices of each data point are consistent.
shapes = []
# Use the row and column indices of 𝑦 to collect the corresponding values from 𝑋
for tif in tifs:
    feature , x_nodatavalue = get_tif_information(tif)[-2:]

    shapes.append(feature.shape)

    feature = feature.astype(np.float32)
    feature[feature == x_nodatavalue] = np.nan
    sample_data = he_findValueAccordingIdx(result , feature , idx_row = 0 , idx_col = 1)

    # Output the sample data.
    output_father = r"E:\Desktop\Python改变地球\A中国滨海湿地处理\9_写出干净的采样数据\arrOutput"
    file_name = os.path.basename(tif).rsplit("." , 1)[0] + ".npy"
    file = os.path.join(output_father , file_name)
    np.save(file = file, arr = sample_data)
    print(f"{file} ------------------------> successfully saved!")
    # break
    del x_nodatavalue , feature


print("所有的tif的shape：" , shapes)
















