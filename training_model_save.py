# -*- coding: utf-8 -*-
"""training_model_save.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bVudFWco2idJXGN982RD0Mod-uIW7LGg
"""

import pandas as pd
import numpy as np
# https://www.kaggle.com/code/carlmcbrideellis/feature-selection-using-the-boruta-shap-package
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from xgboost import XGBClassifier
from sklearn.metrics import f1_score
import random
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import pickle
from sklearn.utils.class_weight import compute_sample_weight

data = pd.read_csv("data_with_new_features.csv")
features = pd.read_csv('feature_importances_xgb.csv', nrows = 20)
features.head()
selected_features = list[features['Unnamed: 0'].values]
selected_features

data_new = data.copy()
y = data_new["default"]
del data_new["default"]

data_new = data_new[selected_features]



df_full_train, df_test, y_full_train, y_test = train_test_split(data_new, y, stratify = y, test_size = 0.2, random_state = 1)

df_train, df_val, y_train, y_val = train_test_split(df_full_train, y_full_train, stratify =y_full_train,  test_size = 0.25, random_state = 1)

df_full_train = df_full_train.reset_index(drop = True)
df_train = df_train.reset_index(drop = True)
df_val = df_val.reset_index(drop = True)
df_test = df_test.reset_index(drop = True)

y_full_train = y_full_train.values
y_train = y_train.values
y_val = y_val.values
y_test = y_test.values

full_train_dicts = df_full_train.to_dict(orient = 'records')
train_dicts = df_train.to_dict(orient = 'records')
val_dicts = df_val.to_dict(orient = 'records')
test_dicts = df_test.to_dict(orient = 'records')

# I was getting a memory error, so I set sparse=True for the DictVectorizer.
dv = DictVectorizer(sparse = True)
dv.fit(train_dicts)
X_full_train_new = dv.transform(full_train_dicts)
X_train_new = dv.transform(train_dicts)
X_val_new = dv.transform(val_dicts)
X_test_new = dv.transform(test_dicts)



sample_weights = compute_sample_weight(class_weight='balanced', y=y_full_train)

# fit model no training data
model = XGBClassifier(params = {'subsample': 0.9, 'scale_pos_weight': 1, 'reg_lambda': 1,'reg_alpha': 0.1, 'n_estimators': 200, 'max_depth': 5,
'learning_rate': 0.05, 'gamma': 0.3, 'colsample_bytree': 0.9}, objective="binary:logistic", feature_name=dv.get_feature_names_out(), random_state = 1)
model.fit(X_full_train_new, y_full_train,sample_weight=sample_weights)

y_pred = model.predict_proba(X_test_new)[:,1]

print(y_pred)

y_pred > 0.5
y_decision = (y_pred >= 0.5).astype(int)
acc = (y_test == y_decision).mean().round(2)
print(f"Accuracy is calculated as \033[1m{acc}\033[0m.")
f_macro = f1_score(y_test, y_decision, average='macro').round(2)
print(f"Macro F1 score is calculated as \033[1m{f_macro}\033[0m.")
f_weighted = f1_score(y_test, y_decision, average='weighted').round(2)
print(f"Weighted F1 score is calculated as \033[1m{f_weighted}\033[0m.")

seeds = [5, 13, 29, 43, 57, 87, 29, 42,1, 93]

#I initiannly get same results for each run. I tried the change subsample, colsample_bytree parameters but it did not help.
#To devaluate non deterministic results I st booster to gblinear readinf the xgboost documentation
#https://readthedocs.org/projects/xgboost/downloads/pdf/latest/

results = []
for i in [5, 13, 29, 43, 57, 87, 28, 42,1, 93]:
    print(i)
    # I have deleted subsample and colsample_bytree parameters since I have evaluated same result at each run
    model = XGBClassifier(params = {'subsample': 0.9, 'scale_pos_weight': 1, 'reg_lambda': 1,'reg_alpha': 0.1, 'n_estimators': 200, 'max_depth': 5,
'learning_rate': 0.05, 'gamma': 0.3, 'colsample_bytree': 0.9}, objective="binary:logitraw", feature_selector= "shuffle", booster = 'gblinear',
                          feature_name=dv.get_feature_names_out(), random_state = i)
    model.fit(X_full_train_new, y_full_train,sample_weight=sample_weights)
    y_pred = model.predict_proba(X_test_new)[:,1]
    y_pred > 0.5
    y_decision = (y_pred >= 0.5).astype(int)
    acc = (y_test == y_decision).mean().round(4)
    print(f"Accuracy is calculated as \033[1m{acc}\033[0m.")
    f_macro = f1_score(y_test, y_decision, average='macro').round(4)
    print(f"Macro F1 score is calculated as \033[1m{f_macro}\033[0m.")
    f_weighted = f1_score(y_test, y_decision, average='weighted').round(4)
    print(f"Weighted F1 score is calculated as \033[1m{f_weighted}\033[0m.")
    results.append((acc,f_macro,f_weighted))
    output_file = f'modelxgb_i={i}.bin'
    with open(output_file, 'wb') as f_out:
        pickle.dump((dv, model), f_out)









model_files = ['modelxgb_i=5.bin', 'modelxgb_i=13.bin', 'modelxgb_i=29.bin', 'modelxgb_i=43.bin', 'modelxgb_i=57.bin', 'modelxgb_i=87.bin',
'modelxgb_i=28.bin', 'modelxgb_i=42.bin',  'modelxgb_i=1.bin', 'modelxgb_i=93.bin']

# Initialize a list to store prediction probabilities
estimations = []

# Define a function to load a model and make predictions
def load_and_predict(file_name, data):
    with open(file_name, 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return model.predict_proba(data)

# Iterate over model files and collect predictions
for model_file in model_files:
    estimations.append(load_and_predict(model_file, X_test_new))


# Alternatively, handle estimations dynamically (e.g., summing probabilities)
y_pred = sum(estimations) / len(estimations)  # Example: averaging

y_pred =y_pred[:,1]
y_pred > 0.5
y_decision = (y_pred >= 0.5).astype(int)
acc = (y_test == y_decision).mean().round(4)
print(f"Accuracy is calculated as \033[1m{acc}\033[0m.")
f_macro = f1_score(y_test, y_decision, average='macro').round(4)
print(f"Macro F1 score is calculated as \033[1m{f_macro}\033[0m.")
f_weighted = f1_score(y_test, y_decision, average='weighted').round(4)
print(f"Weighted F1 score is calculated as \033[1m{f_weighted}\033[0m.")
results.append((acc,f_macro,f_weighted))

# Calculate precision and recall values for different thresholds
precision, recall, thresholds = precision_recall_curve(y_test, y_pred)

# Calculate the average precision score
average_precision = average_precision_score(y_test, y_pred)

# Plot Precision-Recall curve
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, label=f'AP = {average_precision:.2f}', color = "cornflowerblue")
plt.xlabel('Recall', fontsize=12)
plt.ylabel('Precision', fontsize=12)
plt.title('Precision-Recall Curve', fontsize=14)
plt.legend(loc='best', fontsize=12)
plt.grid(alpha=0.4)
plt.show()

xgboost = pd.DataFrame(data = results,columns = ['accuracy', 'f_macro', 'f_weighted'])

xgboost.to_csv('xgboost_results.csv')



"""# Random Forest Classifier"""

results = []
for i in [5, 13, 29, 43, 57, 87, 28, 42,1, 93]:
    print(i)
    # I have deleted subsample and colsample_bytree parameters since I have evaluated same result at each run
    model = RandomForestClassifier(oob_score =  False, n_estimators =  500, min_samples_split = 10, min_samples_leaf = 1, max_samples =  0.9, max_features = 'sqrt', max_depth =  40, class_weight = 'balanced',
                                   bootstrap = True, n_jobs = -1,random_state = i)
    model.fit(X_full_train_new, y_full_train)
    y_pred = model.predict_proba(X_test_new)[:,1]
    y_pred > 0.5
    y_decision = (y_pred >= 0.5).astype(int)
    acc = (y_test == y_decision).mean().round(4)
    print(f"Accuracy is calculated as \033[1m{acc}\033[0m.")
    f_macro = f1_score(y_test, y_decision, average='macro').round(4)
    print(f"Macro F1 score is calculated as \033[1m{f_macro}\033[0m.")
    f_weighted = f1_score(y_test, y_decision, average='weighted').round(4)
    print(f"Weighted F1 score is calculated as \033[1m{f_weighted}\033[0m.")
    results.append((acc,f_macro,f_weighted))
    output_file = f'modelrf_i={i}.bin'
    with open(output_file, 'wb') as f_out:
        pickle.dump((dv, model), f_out)

randomfor = pd.DataFrame(data = results,columns = ['accuracy', 'f_macro', 'f_weighted'])

randomfor.to_csv('randomforest_results.csv')


model_files2 = ['modelrf_i=5.bin', 'modelrf_i=13.bin', 'modelrf_i=29.bin', 'modelrf_i=43.bin', 'modelrf_i=57.bin', 'modelrf_i=87.bin',
'modelrf_i=28.bin', 'modelrf_i=42.bin',  'modelrf_i=1.bin', 'modelrf_i=93.bin']

# Initialize a list to store prediction probabilities
estimations2 = []

# Define a function to load a model and make predictions
def load_and_predict(file_name, data):
    with open(file_name, 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return model.predict_proba(data)

# Iterate over model files and collect predictions
for model_file in model_files2:
    estimations2.append(load_and_predict(model_file, X_test_new))


# Alternatively, handle estimations dynamically (e.g., summing probabilities)
y_pred = sum(estimations2) / len(estimations2)  # Example: averaging

y_pred =y_pred[:,1]
y_pred > 0.5
y_decision = (y_pred >= 0.5).astype(int)
acc = (y_test == y_decision).mean().round(4)
print(f"Accuracy is calculated as \033[1m{acc}\033[0m.")
f_macro = f1_score(y_test, y_decision, average='macro').round(4)
print(f"Macro F1 score is calculated as \033[1m{f_macro}\033[0m.")
f_weighted = f1_score(y_test, y_decision, average='weighted').round(4)
print(f"Weighted F1 score is calculated as \033[1m{f_weighted}\033[0m.")
results.append((acc,f_macro,f_weighted))

# Calculate precision and recall values for different thresholds
precision2, recall2, thresholds2 = precision_recall_curve(y_test, y_pred)

# Calculate the average precision score
average_precision2 = average_precision_score(y_test, y_pred)



"""# Logistic Regression"""


results = []
for i in [5, 13, 29, 43, 57, 87, 28, 42,1, 93]:
    print(i)
    # I have deleted subsample and colsample_bytree parameters since I have evaluated same result at each run
    model = LogisticRegression(class_weight='balanced', random_state = i, solver = 'liblinear', penalty = 'l2', max_iter =500, C = 1, n_jobs = -1)
    model.fit(X_full_train_new, y_full_train)
    y_pred = model.predict_proba(X_test_new)[:,1]
    y_pred > 0.5
    y_decision = (y_pred >= 0.5).astype(int)
    acc = (y_test == y_decision).mean().round(4)
    print(f"Accuracy is calculated as \033[1m{acc}\033[0m.")
    f_macro = f1_score(y_test, y_decision, average='macro').round(4)
    print(f"Macro F1 score is calculated as \033[1m{f_macro}\033[0m.")
    f_weighted = f1_score(y_test, y_decision, average='weighted').round(4)
    print(f"Weighted F1 score is calculated as \033[1m{f_weighted}\033[0m.")
    results.append((acc,f_macro,f_weighted))
    output_file = f'modellog_i={i}.bin'
    with open(output_file, 'wb') as f_out:
        pickle.dump((dv, model), f_out)

logreg = pd.DataFrame(data = results,columns = ['accuracy', 'f_macro', 'f_weighted'])

logreg.to_csv('logreg_results.csv')



a = pd.read_csv('logreg_results.csv')
a.head()


model_files3 = ['modellog_i=5.bin', 'modellog_i=13.bin', 'modellog_i=29.bin', 'modellog_i=43.bin', 'modellog_i=57.bin', 'modellog_i=87.bin',
'modellog_i=28.bin', 'modellog_i=42.bin',  'modellog_i=1.bin', 'modellog_i=93.bin']

# Initialize a list to store prediction probabilities
estimations3 = []

# Define a function to load a model and make predictions
def load_and_predict(file_name, data):
    with open(file_name, 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return model.predict_proba(data)

# Iterate over model files and collect predictions
for model_file in model_files3:
    estimations3.append(load_and_predict(model_file, X_test_new))


# Alternatively, handle estimations dynamically (e.g., summing probabilities)
y_pred = sum(estimations3 )/ len(estimations3)  # Example: averaging

y_pred =y_pred[:,1]
y_pred > 0.5
y_decision = (y_pred >= 0.5).astype(int)
acc = (y_test == y_decision).mean().round(4)
print(f"Accuracy is calculated as \033[1m{acc}\033[0m.")
f_macro = f1_score(y_test, y_decision, average='macro').round(4)
print(f"Macro F1 score is calculated as \033[1m{f_macro}\033[0m.")
f_weighted = f1_score(y_test, y_decision, average='weighted').round(4)
print(f"Weighted F1 score is calculated as \033[1m{f_weighted}\033[0m.")
results.append((acc,f_macro,f_weighted))

# Calculate precision and recall values for different thresholds
precision3, recall3, thresholds2 = precision_recall_curve(y_test, y_pred)

# Calculate the average precision score
average_precision3 = average_precision_score(y_test, y_pred)

# Plot Precision-Recall curve
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, label=f'XGBoost (AP = {average_precision:.2f})', color = "cornflowerblue")
plt.plot(recall2, precision2, label=f'Random Forests (AP = {average_precision2:.2f})', color = "darkred")
plt.plot(recall3, precision3, label=f'Logistic Regression (AP = {average_precision3:.2f})' ,  color = "darkgreen",)
plt.xlabel('Recall', fontsize=12)
plt.ylabel('Precision', fontsize=12)
plt.title('Precision-Recall Curve', fontsize=14)
plt.legend(loc='best', fontsize=12)
plt.grid(alpha=0.4)
plt.savefig('precision_recall_curve.png', bbox_inches='tight')
plt.show()