"""
Created on 2024-11-27

@author: Baoshi He


Machine learning model construction for features with land use change.
"""



import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
# from sklearn.metrics import make_scorer, mean_squared_error, r2_score
from sklearn.metrics import make_scorer, accuracy_score, f1_score
# from xgboost import XGBRegressor
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
import pandas as pd
import joblib
import time
import xgboost as xgb


# load data
data_path = r"C:\Users\123\Desktop\中国滨海湿地建模\finalDataArr\中国滨海湿地最终无nan样本.npy"
data = np.load(data_path)


df = pd.DataFrame(data , columns = ["ROWS" , "COLS" , "Y_CLASS" , "GDP" , "NDVI" , "PET" , "POP" , "TMP" , "BUILT-UP" , "PRE" , "Y" ,"LANDUSE"])

df = df[df["Y_CLASS"] != 0]

df["Y_CLASS"] = df["Y_CLASS"].replace(3 , 5)
df["Y_CLASS"] = df["Y_CLASS"].replace(2 , 4)
df["Y_CLASS"] = df["Y_CLASS"].replace(1 , 3)
df["Y_CLASS"] = df["Y_CLASS"].replace(-3 , 0)
df["Y_CLASS"] = df["Y_CLASS"].replace(-2 , 1)
df["Y_CLASS"] = df["Y_CLASS"].replace(-1 , 2)

df["LANDUSE"] = df["LANDUSE"].astype('int16').astype('str')


X = df.loc[: , ["GDP" , "NDVI" , "PET" , "POP" , "TMP" , "BUILT-UP" , "PRE" ,"LANDUSE"]]
# X = df.loc[: , ["GDP" , "NDVI" , "PET" , "POP" , "TMP" , "BUILT-UP" , "PRE"]]
y = df.loc[: , ["Y_CLASS"]]
X , y
print('y的信息:' , y.value_counts())


# set train and test dataset
X_train , X_test , y_train , y_test = train_test_split(X , y , test_size = 0.3 , random_state=42)


numeric_features = ["GDP" , "NDVI" , "PET" , "POP" , "TMP" , "PRE"]
categorical_features = ["LANDUSE"]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),  
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)  # One-Hot
        # binary_feature 
    ], remainder='passthrough')


pipe_xgb = Pipeline([
    ('preprocessor', preprocessor),
    ('xgb', XGBClassifier(objective='multi:softmax', 
                         random_state=42 ,
                         num_class=6,                 
                         tree_method = 'hist' ,      
                         device = 'cuda'      
                        #  device = 'cpu' 
                         ))
])


# piple
param_grid = {
    'xgb__n_estimators': [100, 200, 300 , 400],
    'xgb__learning_rate': [0.01, 0.1, 0.2 , 0.3, 0.5 , 0.9],
    'xgb__max_depth': [3, 5, 7 ,9 ,11 ,13 , 15 , 20],
    'xgb__subsample': [0.5 , 0.7, 0.8, 1.0],
    'xgb__colsample_bytree': [0.3 , 0.5 , 0.7, 0.8, 1.0]
}



# Calculate the parameter space size.
no_option = 1
for i in param_grid:
    no_option *= len(param_grid)
print("参数空间：" , no_option)


scoring = {
    'accuracy': make_scorer(accuracy_score),
    'f1_macro': make_scorer(f1_score, average='macro')
}


# K-fold cross-validation.
kfold = KFold(n_splits=5, shuffle=True, random_state=42)


# GridSearchCV
grid_search = GridSearchCV(estimator = pipe_xgb,
                           param_grid = param_grid,
                           scoring = scoring, 
                           cv=kfold,
                        #    verbose=1,
                           verbose=2,   
                           n_jobs=-1 , 
                           refit='accuracy', 
                           )


start = time.time()

grid_result = grid_search.fit(X_train, y_train)


print(f"模型训练用时：{time.time() - start}s")
print(f"最佳交叉验证得分 (Accuracy): {grid_search.cv_results_['mean_test_accuracy'][grid_search.best_index_]}")
print(f"最佳交叉验证得分 (F1 Macro): {grid_search.cv_results_['mean_test_f1_macro'][grid_search.best_index_]}")

# save model
model_name = r'C:\Users\123\Desktop\中国滨海湿地建模\10_Xgboost建模\输出模型\中国滨海湿地影响因素建模_XGB_带土地利用.joblib'
joblib.dump(grid_search, model_name)
print(f"{model_name} --------------------> successfully saved!!!")

# ################################ test ################################
# Use the best model to make predictions on the test set and calculate accuracy and F1 score.
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

accuracy_test_score = accuracy_score(y_test, y_pred)
f1_test_score = f1_score(y_test, y_pred, average='macro')

print(f"测试集准确率得分: {accuracy_test_score}")
print(f"测试集F1 Macro得分: {f1_test_score}")








