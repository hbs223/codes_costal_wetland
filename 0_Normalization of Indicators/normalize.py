"""
Created on 2024-11-27

@author: Baoshi He


This program is used for normalization calculation.
"""


import numpy as np
from readAndWriteGeotif import *
import os



def concate(year2000_arr , year2020_arr):

    print("去除nan后的数据拼接................................................................")

    noNanData_2000 = year2000_arr.flatten()[~np.isnan(year2000_arr.flatten())]
    noNanData_2020 = year2020_arr.flatten()[~np.isnan(year2020_arr.flatten())]


    noNanData = np.concatenate([noNanData_2000, noNanData_2020])

    return noNanData



def normalize_maxMinValue(noNatData):

    print("正在全局归一化.....................................................................")

    # 传入的数据已经没有nan了
    max_value = np.max(noNatData)
    min_value = np.min(noNatData)


    return max_value, min_value


def normalize(max_value, min_value , year_arr , direction = "positive"):
    # positive
    if direction == "positive":

        normalize_year_arr = (year_arr - min_value) / (max_value - min_value)

        # return normalize_year_arr

    # negetive
    elif direction == "negetive":
        normalize_year_arr = (max_value - year_arr) / (max_value - min_value)

    else:
        print("please input true direction parameter!")

    return normalize_year_arr


def get_file_path(floder_path , suffix = ".tif"):  # 这里默认是找到文件下所有tif结尾的文件（包含子文件夹）
    file_list = []
    for file_path,sub_dirs1,files in os.walk(floder_path):
        # print(file_path,sub_dirs1,files)
        # print("-"*60)
        for file in files:
            # print(file)
            if file.endswith(suffix):
                tif_full_path = file_path + '\\' + file
                # tif_full_path = os.path.join(file_path , file)       # 这个和上面那行实现的效果是一样的
                # print(tif_full_path)
                file_list.append(tif_full_path)
    return file_list





if __name__ == "__main__":


    a = np.arange(16).reshape(4 , 4).astype(float)
    a[1,1] = np.nan
    print("a: ", a)

    b = np.arange(9).reshape(3 , 3).astype(float)
    b[0,0] = np.nan
    print("b: ", b)

    noNanData = concate(a , b)

    print("去除nan后放在一起的数据:" , noNanData)






























