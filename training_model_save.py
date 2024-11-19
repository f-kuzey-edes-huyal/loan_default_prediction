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






model_file1 = 'modelxgb_i=5.bin'

with open(model_file1, 'rb') as f_in:
    dv1, model1 = pickle.load(f_in)

est1 = model1.predict_proba(X_test_new)

model_file2 = 'modelxgb_i=13.bin'

with open(model_file2, 'rb') as f_in:
    dv2, model2 = pickle.load(f_in)

est2 = model2.predict_proba(X_test_new)

model_file3 = 'modelxgb_i=29.bin'

with open(model_file3, 'rb') as f_in:
    dv3, model3 = pickle.load(f_in)

est3 = model3.predict_proba(X_test_new)


model_file4 = 'modelxgb_i=43.bin'

with open(model_file4, 'rb') as f_in:
    dv4, model4 = pickle.load(f_in)

est4 = model4.predict_proba(X_test_new)


model_file5 = 'modelxgb_i=57.bin'

with open(model_file5, 'rb') as f_in:
    dv5, model5 = pickle.load(f_in)

est5 = model5.predict_proba(X_test_new)



model_file6 = 'modelxgb_i=87.bin'

with open(model_file6, 'rb') as f_in:
    dv6, model6 = pickle.load(f_in)

est6 = model6.predict_proba(X_test_new)


model_file7 = 'modelxgb_i=28.bin'

with open(model_file7, 'rb') as f_in:
    dv7, model7 = pickle.load(f_in)

est7 = model7.predict_proba(X_test_new)


model_file8 = 'modelxgb_i=42.bin'

with open(model_file8, 'rb') as f_in:
    dv8, model8 = pickle.load(f_in)

est8 = model8.predict_proba(X_test_new)


model_file9 = 'modelxgb_i=1.bin'

with open(model_file9, 'rb') as f_in:
    dv9, model9 = pickle.load(f_in)

est9 = model9.predict_proba(X_test_new)

model_file10 = 'modelxgb_i=93.bin'

with open(model_file10, 'rb') as f_in:
    dv10, model10 = pickle.load(f_in)

est10 = model10.predict_proba(X_test_new)

list_models = np.array([est1, est2, est3, est4, est5, est6, est7, est8, est9, est10])
averages = np.average(list_models, axis=0)

y_pred_proba = est1
y_pred =averages[:,1]
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

