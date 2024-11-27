"""
Created on 2024-11-27

@author: Baoshi He


Calculate and plot the SHAP values for each class.
"""

import numpy as np
import matplotlib.pyplot as plt
import shap
from matplotlib.ticker import AutoMinorLocator
from matplotlib import rcParams

# Load data
shap_values = np.load(r"E:\Desktop\Python改变地球\A中国滨海湿地处理\12_shap分析\output\shap_values_6000采样点.npy")
X_transformed = np.load(r"E:\Desktop\Python改变地球\A中国滨海湿地处理\12_shap分析\output\X_transformed_6000采样点.npy")
feature_names = ['GDP', 'NDVI', 'PET', 'POP', 'TMP', 'BUILT-UP', 'PRE']


level = 1       # Set different categories separately.


shap_values_for_class_0 = shap_values[:, :, level] 



######################### plot #########################
rcParams['axes.unicode_minus'] = False  
rcParams['font.serif'] = ['Times New Roman']  
plt.rcParams['font.sans-serif'] = ['Times New Roman']  

dpi = 600 
fig, ax = plt.subplots(figsize=(6, 7), dpi=dpi, facecolor='none')


shap.summary_plot(
    shap_values_for_class_0,  
    X_transformed,            
    feature_names=feature_names,  
    plot_type="dot",         
    color_bar=False,          
    cmap='cividis',           
    show=False,               
    plot_size=None,          
)


for line in ax.lines:
    if line.get_xdata()[0] == 0 and line.get_linestyle() == '--':
        line.remove()


ax.axvline(x=0, color='white', linestyle='--', linewidth=2)  # 添加白色虚线

ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7, color='white')  # 设置网格线样式

ax.spines['top'].set_color('white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')

ax.yaxis.set_minor_locator(AutoMinorLocator(0))  # 在主刻度之间添加次刻度

ax.set_xlabel('SHAP value (impact on model output)', fontsize=16, color='white')
ax.set_ylabel('Features', fontsize=16, color='white')

ax.tick_params(axis='x', labelsize=14, colors='white')
ax.tick_params(axis='y', labelsize=14, colors='white')

plt.tight_layout()
saveName = r"E:\Desktop\Python改变地球\A中国滨海湿地处理\制图\分类的shap图\output\shap图_类别{}_用在流程图中.tif".format(level)
plt.savefig(saveName, format='tiff', dpi=dpi, bbox_inches='tight', pad_inches=0.1, transparent=True)

plt.show()