"""
Created on 2024-11-27

@author: Baoshi He


Output the land use change types and their feature importance to an Excel file.
"""



import numpy as np
import matplotlib.pyplot as plt
import joblib
import xgboost as xgb
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd

# load XGBoost moedel
model_path = r'E:\Desktop\Python改变地球\A中国滨海湿地处理\10_Xgboost建模\输出模型\中国滨海湿地影响因素建模_XGB_带土地利用.joblib'
loaded_model = joblib.load(model_path)

preprocessor = loaded_model.best_estimator_.named_steps['preprocessor']
xgb_model = loaded_model.best_estimator_.named_steps['xgb']

# feature name
numeric_features = ["GDP", "NDVI", "PET", "POP", "TMP", "BUILT-UP", "PRE"]

categorical_features = preprocessor.named_transformers_['cat'].get_feature_names_out(['LANDUSE'])

all_features = list(numeric_features) + list(categorical_features)

importances = xgb_model.feature_importances_

# Obtain the top 10 features by importance and their corresponding importance scores.
indices = np.argsort(importances)[-10:][::-1] 
top_features = [all_features[i] for i in indices]
top_importances = importances[indices]

print("Top 10 important features:")
for feature, importance in zip(top_features, top_importances):
    print(f"{feature}: {importance:.4f}")


# output data
df = pd.DataFrame(columns = ["change type" , "feature importance"])
df["change type"] = top_features
df["feature importance"] = top_importances

df_name = r"E:\Desktop\Python改变地球\A中国滨海湿地处理\制图\XGBoost模型特征重要性绘图\output\变化类型和特征重要性.xlsx"
df.to_excel(df_name)

print(df)
print(f"{df_name} -------------------> successfully!")



# Simple visualization of the Top 10 Feature Importance.
plt.figure(figsize=(10, 6))
plt.barh(top_features, top_importances, color='skyblue')
plt.xlabel('Feature Importance')
plt.title('Top 10 Feature Importance')
plt.gca().invert_yaxis()
plt.show()