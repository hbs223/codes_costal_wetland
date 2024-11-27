"""
Created on 2024-11-27

@author: Baoshi He


Plot the mean with error bars and the feature importance chart.
"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns


def get_file_path(floder_path , suffix = ".tif"):  
    file_list = []
    for file_path,sub_dirs1,files in os.walk(floder_path):
        # print(file_path,sub_dirs1,files)
        # print("-"*60)
        for file in files:
            # print(file)
            if file.endswith(suffix):
                tif_full_path = file_path + '\\' + file
                file_list.append(tif_full_path)
    return file_list



def repalceName(col_value):   # df["value"]

    n_col_value = col_value.replace("7211" , "Paddy field--->Marsh") \
            .replace("1271" , "Permanent water--->Dryland") \
            .replace("1171" , "Permanent water--->Paddy field") \
            .replace("7145" , "Tidal flat--->Permanent water") \
            .replace("7171" , "Permanent water--->Permanent water") \
            .replace("5145" , "Tidal flat--->City") \
            .replace("7176" , "Salt marsh--->Permanent water") \
            .replace("6471" , "Permanent water--->Swamp") \
            .replace("4611" , "Paddy field--->Flooded flat") \
            .replace("7263" , "Saline--->Marsh") 


    return n_col_value


# load data
file_path = r'E:\Desktop\Python改变地球\A中国滨海湿地处理\制图\XGBoost模型特征重要性绘图\output\绘制变化类型和特征重要性和均值和误差棒.xlsx'  # 请替换为你的数据文件路径
df = pd.read_excel(file_path , index_col = 0)

df['type'] = repalceName(col_value = df['value'].astype(str))

print(df)

types = df['type']
values = df['value'].astype(str)
means = df['mean']
# std_errors = df['standard_error']
feature_importance = df['feature importance']
std_devs = df["std_dev"]


npys = get_file_path(floder_path = r"E:\Desktop\Python改变地球\A中国滨海湿地处理\制图\XGBoost模型特征重要性绘图\output" , suffix = ".npy")

violin_df = pd.DataFrame()


N = 1

for code in df["value"]:
    npy = r'E:\\Desktop\\Python改变地球\\A中国滨海湿地处理\\制图\\XGBoost模型特征重要性绘图\\output\\{}_生态质量变化.npy'.format(code)
    arr = np.sort(np.load(npy))

    df_temp = pd.DataFrame(arr[::N] , columns = ["Value"])
    df_temp['fea_name'] = str(code)

    violin_df = pd.concat([violin_df , df_temp] ,  ignore_index=True)
violin_df["type"] = repalceName(violin_df["fea_name"].astype(str))
print(violin_df)


# color
positive_error_bar_color = "#1f77b4" 
negative_error_bar_color = "#E07A5F"
violin_color = "#CBD5E1"


plt.rcParams['axes.unicode_minus'] = False 
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.sans-serif'] = ['Times New Roman'] 


dpi = 1000

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True, gridspec_kw={'height_ratios': [1.8, 1]} ,dpi = dpi)


positive_plotted = False
negative_plotted = False

for i in range(len(means)):
    if means[i] >= 0:
        ax1.errorbar(x=values[i], y=means[i], yerr=std_devs[i], fmt='o', color=positive_error_bar_color, ecolor=positive_error_bar_color, elinewidth=2, capsize=4 , label='Mean > 0' if not positive_plotted else "")
        positive_plotted = True
    else:
        ax1.errorbar(x=values[i], y=means[i], yerr=std_devs[i], fmt='o', color=negative_error_bar_color, ecolor=negative_error_bar_color, elinewidth=2, capsize=4 , label='Mean < 0' if not negative_plotted else "")
        negative_plotted = True


ax1.set_ylabel('Mean with Standard Error', fontsize=14)

ax1.axhline(y=0, color='grey', linestyle='--', linewidth=1)

sns.violinplot(x='fea_name', y='Value', data=violin_df, ax=ax1, inner=None, color=violin_color, scale="width" , linewidth=0)

ax1.set_xlabel("")
ax1.set_ylabel(r'$\Delta$ CEQI', fontsize=16)


ax1.set_ylim(violin_df["Value"].min(), violin_df["Value"].max())
ax1.tick_params(axis='x', direction='in')
ax1.tick_params(axis='x', labelsize=14)
ax1.tick_params(axis='y', labelsize=14)

# grid
handles, labels = ax1.get_legend_handles_labels()
if len(handles) > 0 and len(labels) > 0:
    ax1.legend(handles, labels, loc='lower right', fontsize=16  ,frameon=False)


bars = ax2.bar(values, feature_importance, color='skyblue', width=0.6)
ax2.set_ylabel('Feature Importance', fontsize=16)

ax2.set_xlabel('Land Use Change Type', fontsize=16)

ax2.set_ylim(0, max(feature_importance) + 0.01)

ax2.set_xticks(np.arange(len(types)))

ax2.set_xticklabels([])
ax2.tick_params(axis='x', direction='in')

ax2.tick_params(axis='x', labelsize=14)
ax2.tick_params(axis='y', labelsize=14)


# add text labels
for bar, label in zip(bars, types):
    ax2.text(bar.get_x() + bar.get_width() / 2, 0.002, label, ha='center', va='bottom', fontsize=14, rotation=90)


ax1.text(0.05,0.98, '(a)', transform=ax1.transAxes, fontsize=20, va='top', ha='right')  
  
ax2.text(0.05,0.98, '(b)', transform=ax2.transAxes, fontsize=20, va='top', ha='right')  
  
plt.tight_layout()


################################################################################################################
saveName = r"E:\Desktop\Python改变地球\A中国滨海湿地处理\制图\XGBoost模型特征重要性绘图\output\XGBoost特征重要性_{}dpi_修改Y轴label.tif".format(dpi)
plt.savefig(saveName , format='tiff' , dpi = dpi , bbox_inches='tight', pad_inches=0.1)

plt.show()
