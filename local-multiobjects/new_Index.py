import pandas as pd
import numpy as np
from scipy.linalg import inv
import matplotlib.pyplot as plt


def normalize(data):
    min_val = np.min(data)
    max_val = np.max(data)
    normalized_data = 2 * (data - min_val) / (max_val - min_val) - 1
    return normalized_data


def calculate_jm(aver1, aver2, cov1, cov2):
    m = np.abs(aver1 - aver2) ** 2 / (cov1 + cov2)
    d = np.abs(cov1 + cov2) / (np.sqrt(np.abs(cov1 * cov2)) * 2)
    b = 0.125 * m + 0.5 * np.log(d)
    jm = 2 * (1 - np.exp(-1 * b))   #采用原始定义的JM距离
    return jm


def calculate_jm_distance(dataframe, feature):
    two_data = dataframe[['mangrove', feature]]

    # 提取反射率数据
    reflectance_mangrove = two_data['mangrove'].values.reshape(-1, 1)
    reflectance_feature = two_data[feature].values.reshape(-1, 1)

    # 计算均值向量
    mean_mangrove = np.mean(reflectance_mangrove, axis=0)[0]
    mean_feature = np.mean(reflectance_feature, axis=0)[0]

    # 计算方差
    cov_mangrove = np.cov(reflectance_mangrove, rowvar=False)
    cov_feature = np.cov(reflectance_feature, rowvar=False)

    # 计算 JM 距离
    jm_distance = calculate_jm(mean_mangrove, mean_feature, cov_mangrove, cov_feature)

    return jm_distance


channel_names = ['red', 'green', 'blue', 'nir', 'swir1', 'swir2']
features = ['mangrove', 'vegetation', 'plough', 'paddyfield', 'water', 'architecture']
dfs = {}  # 使用字典来存储数据框

# 批量导入文件
for channel_name in channel_names:
    file_path = f'{channel_name}_channel_terrain_classification.csv'
    df = pd.read_csv(file_path)
    # 存储到字典中，键为通道名
    dfs[channel_name] = df
'''
# 通道
JM1 = np.zeros((len(features), len(channel_names)))
# 外部循环遍历通道
for i, channel_name in enumerate(channel_names):
    df = dfs[channel_name]
    # 内部循环遍历地物类别
    for j, feature in enumerate(features):
        jm_distance = calculate_jm_distance(df, feature)
        JM1[i, j] = jm_distance

# Create a figure
plt.rcParams["font.family"] = "Times New Roman"
fig, ax = plt.subplots(figsize=(6, 4))
markers = ['o', 'D', '^', 'o', 'D', '^']
fillstyles = ['none', 'none', 'none', 'full', 'full', 'full']
for i in range(len(channel_names)):
    ax.plot(features, JM1[i, :], label=channel_names[i], marker=markers[i], fillstyle=fillstyles[i], linestyle='-')
ax.set_xlabel('Land Cover Types')
ax.set_ylabel('JM Distance')
ax.set_title('JM Distances Between Land Cover Types And Mangroves')
ax.legend()
plt.savefig("不同通道反射率对地物的JM距离.png", dpi=300)
plt.show()
'''
# 指数
index_names = ['NDVI', 'NDWI', 'LSWI1', 'LSWI2', 'EMSI', 'MVI1', 'MVI2', 'new']
dfs['NDVI'] = (dfs['nir'] - dfs['red']) / (dfs['nir'] + dfs['red'])
dfs['NDWI'] = (dfs['nir'] - dfs['green']) / (dfs['nir'] + dfs['green'])
dfs['LSWI1'] = (dfs['nir'] - dfs['swir1']) / (dfs['nir'] + dfs['swir1'])
dfs['LSWI2'] = (dfs['nir'] - dfs['swir2']) / (dfs['nir'] + dfs['swir2'])
dfs['EMSI'] = dfs['NDVI'] * (dfs['swir1'] - dfs['swir2']) / (dfs['swir1'] + dfs['swir2'])
dfs['MVI1'] = (dfs['nir'] - dfs['green']) / (dfs['swir1'] - dfs['green'])
dfs['MVI2'] = (dfs['nir'] - dfs['green']) / (dfs['swir2'] - dfs['green'])
# dfs['new'] = (dfs['MVI1'] - dfs['EMSI']) / (dfs['MVI2'] )
# dfs['new'] = ((dfs['nir'] - dfs['red']) / (dfs['swir1'] - dfs['green'])) * dfs['nir']
dfs['new'] = (dfs['nir']) / (2.5 * dfs['swir1'] + dfs['swir2'])

dfs['EMSI'] = normalize(dfs['EMSI'])
print('EMSI\n', dfs['EMSI'].describe())
dfs['MVI1'] = normalize(dfs['MVI1'])
print('MVI1\n', dfs['MVI1'].describe())
dfs['MVI2'] = normalize(dfs['MVI2'])
print('MVI2\n', dfs['MVI2'].describe())
dfs['new'] = normalize(dfs['new'])
print('new\n', dfs['new'].describe())

JM2 = np.zeros((len(index_names), len(features)))
# 外部循环遍历通道
for i, index_name in enumerate(index_names):
    df = dfs[index_name]
    # 内部循环遍历地物类别
    for j, feature in enumerate(features):
        jm_distance = calculate_jm_distance(df, feature)
        JM2[i, j] = jm_distance

# Create a figure
plt.rcParams["font.family"] = "Times New Roman"
fig, ax = plt.subplots(figsize=(6, 4))
markers = ['o', 'D', '^', 's', 'o', 'D', '^', 's']
fillstyles = ['none', 'none', 'none', 'none', 'full', 'full', 'full', 'full']
for i in range(len(index_names)):
    ax.plot(features, JM2[i, :], label=index_names[i], marker=markers[i], fillstyle=fillstyles[i], linestyle='-')
ax.set_xlabel('Land Cover Types')
ax.set_ylabel('JM Distance')
ax.set_title('JM Distances Between Land Cover Types And Mangroves')
ax.legend()
plt.savefig("不同指数对地物的JM距离.png", dpi=300)
plt.show()
