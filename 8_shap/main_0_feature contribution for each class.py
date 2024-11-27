"""
Created on 2024-11-27

@author: Baoshi He


Calculate and plot the feature contribution for each class.
"""



import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
# import shap
from matplotlib.ticker import AutoMinorLocator
from matplotlib import rcParams
import pandas as pd

# load data
shap_values = np.load(r"E:\Desktop\Python改变地球\A中国滨海湿地处理\12_shap分析\output\shap_values_6000采样点.npy")
X_transformed = np.load(r"E:\Desktop\Python改变地球\A中国滨海湿地处理\12_shap分析\output\X_transformed_6000采样点.npy")
feature_names = ['GDP', 'NDVI', 'PET', 'POP', 'TMP', 'BUILT-UP', 'PRE']

# Extract the SHAP values for each class.
shap_values_class_0 = shap_values[:, :, 0]
shap_values_class_1 = shap_values[:, :, 1]
shap_values_class_2 = shap_values[:, :, 2]
shap_values_class_3 = shap_values[:, :, 3]
shap_values_class_4 = shap_values[:, :, 4]
shap_values_class_5 = shap_values[:, :, 5]

# Calculate the feature contribution for each class.
importance_class_0 = np.abs(shap_values_class_0).mean(axis=0)
importance_class_1 = np.abs(shap_values_class_1).mean(axis=0)
importance_class_2 = np.abs(shap_values_class_2).mean(axis=0)
importance_class_3 = np.abs(shap_values_class_3).mean(axis=0)
importance_class_4 = np.abs(shap_values_class_4).mean(axis=0)
importance_class_5 = np.abs(shap_values_class_5).mean(axis=0)

print("shap_values_class_0.shape:", shap_values_class_0.shape)  # (6000, 7)

importance_df = pd.DataFrame({
    '类别0': importance_class_0,
    '类别1': importance_class_1,
    '类别2': importance_class_2,
    '类别3': importance_class_3,
    '类别4': importance_class_4,
    '类别5': importance_class_5}, index=feature_names)

# Rename columns based on the Type and Type_encoded mapping table.
type_mapping = {0: '-3', 1: '-2', 2: '-1', 3: '1', 4: '2', 5: '3'}
importance_df.columns = [type_mapping[int(col.split('类别')[1])] for col in importance_df.columns]

print(importance_df)


importance_df['row_sum'] = importance_df.sum(axis=1)

sorted_importance_df = importance_df.sort_values(by='row_sum', ascending=True)

sorted_importance_df = sorted_importance_df.drop(columns=['row_sum'])
elements = sorted_importance_df.index

# color
custom_colors = {
    '-3': (168/255, 0, 0), 
    '-2': (255/255, 0, 0),   
    '-1': (255/255, 190/255, 190/255),
    '1': (190/255, 210/255, 255/255),  
    '2': (0, 112/255, 255/255),        
    '3': (76/255, 0, 115/255)       
}

colors = [custom_colors[col] for col in sorted_importance_df.columns]


############################## plot ###########################################
rcParams['axes.unicode_minus'] = False  
rcParams['font.serif'] = ['Times New Roman']  
plt.rcParams['font.sans-serif'] = ['Times New Roman']




dpi = 1000

fig, ax = plt.subplots(figsize=(12, 6), dpi=dpi)

bottom = np.zeros(len(elements))


for i, column in enumerate(sorted_importance_df.columns):
    ax.barh(sorted_importance_df.index,     
            sorted_importance_df[column],  
            left=bottom,                   
            color=colors[i],              
            label=column             
            )    
    bottom += sorted_importance_df[column]



ax.set_xlabel('Mean|SHAP Value|', fontsize=16)


ax.set_yticks(np.arange(len(elements)))
ax.set_yticklabels(elements, fontsize=10)


for i, el in enumerate(elements):
    ax.text(bottom[i], i, ' ' + str(el), va='center', fontsize=14 , rotation=-90)



fig.text(0.51, 0.15, 'Feature Importance', ha='center', fontsize=18, color='black')

ax.legend(frameon=False , title='Change level', fontsize=14, title_fontsize=14)


ax.set_yticks([]) 
ax.set_yticklabels([])  
ax.set_ylabel('')


plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.tight_layout()

################################################################################################################
saveName = r"E:\Desktop\Python改变地球\A中国滨海湿地处理\制图\分类的shap图\output\分类的Mean_shap.tif"
plt.savefig(saveName , format='tiff' , dpi = dpi , bbox_inches='tight', pad_inches=0.1)

plt.show()