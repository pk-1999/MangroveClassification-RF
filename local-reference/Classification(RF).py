import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import cohen_kappa_score
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt


def normalize(data):
    min_val = np.min(data)
    max_val = np.max(data)
    normalized_data = (data - min_val) / (max_val - min_val)
    return normalized_data


df = pd.read_csv("Points-20-1.csv")
factors = ['landcover', 'red', 'green', 'blue', 'nir', 'swir1', 'swir2']
df = df[factors]


# 计算NDVI
df['NDVI'] = (df['nir'] - df['red']) / (df['nir'] + df['red'])

# 计算NDWI
df['NDWI'] = (df['nir'] - df['green']) / (df['nir'] + df['green'])

# 计算LSWI
df['LSWI1'] = (df['nir'] - df['swir1']) / (df['nir'] + df['swir1'])
df['LSWI2'] = (df['nir'] - df['swir2']) / (df['nir'] + df['swir2'])

# 计算EMSI
df['EMSI'] = (df['swir1'] - df['swir2']) / (df['swir1'] + df['swir2'])
# df['EMSI'] = 2 * (df['nir'] + df['swir1']) * (df['swir1'] + df['swir2'])

# 计算MVI
df['MVI1'] = (df['nir'] - df['green']) / (df['swir1'] - df['green'])
df['MVI2'] = (df['nir'] - df['green']) / (df['swir2'] - df['green'])

# 手搓！
df['new'] = df['nir'] / (2.5 * df['swir1'] + df['swir2'])

inf_mask = df.applymap(lambda x: np.isinf(x) or np.isnan(x))
df = df.drop(df[inf_mask.any(axis=1)].index)

df[['red', 'green', 'blue']] = df[['red', 'green', 'blue']] * 4
df['nir'] = df['nir'] * 1.5
df['swir1'] = df['swir1'] * 2
df['swir2'] = df['swir2'] * 3
df['new'] = normalize(df['new'])

features = ['landcover', 'red', 'green', 'blue', 'nir', 'swir1', 'swir2']
# features = ['landcover','NDVI','NDWI','LSWI1','LSWI2','new']
# features = ['landcover', 'nir', 'swir1', 'swir2', 'EMSI']
data = df[features]
print(data.describe())

# 检查缺失值并删除包含缺失值的行
data.dropna(inplace=True)

# 划分训练集
X = data.drop(columns=['landcover'])
y = data['landcover']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=100)

# 通过交叉验证寻找最佳的 n_estimators
best_kappa = -1
best_n_estimators = 0

for n_estimators in range(10, 210, 10):
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=300)
    y_pred_cv = cross_val_predict(model, X_train, y_train, cv=5)
    kappa = cohen_kappa_score(y_train, y_pred_cv)

    print(f"n_estimators = {n_estimators}, Kappa Score: {kappa}")

    if kappa > best_kappa:
        best_kappa = kappa
        best_n_estimators = n_estimators

# 使用最佳的 n_estimators 训练最终模型
final_model = RandomForestClassifier(n_estimators=best_n_estimators, random_state=300)
final_model.fit(X_train, y_train)

# 在测试集上评估最终模型
y_pred = final_model.predict(X_test)

# 计算并输出最终模型的 Kappa 系数
final_kappa = cohen_kappa_score(y_test, y_pred)
print(f"\nBest n_estimators: {best_n_estimators}")
print("Final Model Kappa Score:", final_kappa)

# 评估各变量重要性
selector = SelectFromModel(final_model, threshold=0.15)   #决定系数
importances = selector.get_support()
for j in range(1,len(features)):
    print(features[j] + '\t' + str(final_model.feature_importances_[j-1]), end='\t')
    if importances[j-1]:
        print('important')
    else:
        print()

feature_importance = final_model.feature_importances_
plt.figure(figsize=(10, 6))
plt.bar(X.columns, feature_importance)
plt.title('Feature Importance')
plt.xlabel('Features')
plt.ylabel('Importance')
plt.show()

'''
# 添加NDVI,EVI特征
data['NDVI'] = (data['nir'] - data['red']) / (data['nir'] + data['red']).where((data['nir'] + data['red']) != 0, pd.NA)
#data['EVI'] = (data['nir'] - data['red']) / (data['nir'] + 6*data['red'] - 7.5*data['blue'] + 1).where((data['nir'] + data['red']) != 0, pd.NA)

#划分训练集
X_expand = data.drop(columns=['landcover'])
X_expand_train, X_expand_test, y_expand_train, y_expand_test = train_test_split(X_expand, y, test_size=0.20, random_state=10)

#RF
model_expand = RandomForestClassifier(n_estimators=200)
model_expand.fit(X_expand_train, y_expand_train)

# 在测试集上评估模型
y_expand_pred = model_expand.predict(X_expand_test)

# 计算评估指标
print("\n考虑添加 NDVI 和 EVI 进行预测")
print("Accuracy:", metrics.accuracy_score(y_expand_test, y_expand_pred))
print("Precision:", metrics.precision_score(y_expand_test, y_expand_pred))
print("Recall:", metrics.recall_score(y_expand_test, y_expand_pred))
print("F1 Score:", metrics.f1_score(y_expand_test, y_expand_pred))
# 计算并输出 Kappa 系数
kappa_expand = cohen_kappa_score(y_expand_test, y_expand_pred)
print("Kappa Score:", kappa_expand)


# 评估各变量重要性
features_expand = ['landcover', 'red', 'green', 'blue', 'nir', 'NDVI'] #, 'EVI'
#features_expand = ['landcover', 'NDVI', 'EVI']
selector = SelectFromModel(model_expand, threshold=0.15)   #决定系数
importances = selector.get_support()
for j in range(1,len(features_expand)):
    print(features_expand[j] + '\t' + str(model_expand.feature_importances_[j-1]), end='\t')
    if importances[j-1]:
        print('important')
    else:
        print()
'''
