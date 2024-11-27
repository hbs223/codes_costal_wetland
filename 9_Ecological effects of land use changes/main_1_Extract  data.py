"""
Created on 2024-11-27

@author: Baoshi He


Use land use change types to obtain the CEQI change values and output the data.
"""




import pandas as pd
import numpy as np
from readAndWriteGeotif import *



df = pd.read_excel(r"E:\Desktop\Python改变地球\A中国滨海湿地处理\制图\XGBoost模型特征重要性绘图\output\变化类型和特征重要性.xlsx" , index_col = 0)


# Create fields
df["value"] = df['change type'].str.split('_').str[1]
df["mean"] = 0
df["std_dev"] = 0
df["standard_error"] = 0




change_path = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\影响因素_行列号对齐_相减\土地利用变化_相加\中国滨海湿地土地利用变化_2020扩大100倍_20202000.tif"
im_width,im_height,im_bands,im_geotrans,im_proj,im_data_lucc , nodatavalue_lucc = get_tif_information(file_path = change_path)

eco_change_path = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\最终评估结果\中国滨海湿地生态质量综合评估_20002020_差值_v2_python计算结果.tif"
im_width,im_height,im_bands,im_geotrans,im_proj,im_data_ec , nodatavalue_ec = get_tif_information(file_path = eco_change_path)

im_data_ec[im_data_ec == nodatavalue_ec] = np.nan


for val in df["value"]:

    mask = im_data_lucc == int(val)
    data = im_data_ec[mask]
    data = data[~np.isnan(data)]

    # output data to plot violin fig.
    saveName = r"E:\Desktop\Python改变地球\A中国滨海湿地处理\制图\XGBoost模型特征重要性绘图\output\{}_生态质量变化.npy".format(val)
    np.save(saveName , data)

    print(f"{saveName} ---------------------> successfully!")


    # calculate mean value
    mean_value = np.mean(data)
    # calculate standard_error value
    std_dev = np.std(data) 
    standard_error = np.std(data) / np.sqrt(len(data))


    df.loc[df["value"] == val , "mean"] = mean_value
    df.loc[df["value"] == val , "std_dev"] = std_dev
    df.loc[df["value"] == val , "standard_error"] = standard_error


    print(f"{val}均值: {mean_value}")
    print(f"{val}标准差: {std_dev}")
    print(f"{val}标准误差: {standard_error}")

    # break

print(df)
df.to_excel(r"E:\Desktop\Python改变地球\A中国滨海湿地处理\制图\XGBoost模型特征重要性绘图\output\绘制变化类型和特征重要性和均值和误差棒.xlsx")