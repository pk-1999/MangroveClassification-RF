import pandas as pd
import numpy as np
from scipy.linalg import inv
import matplotlib.pyplot as plt


def calculate_jm(aver1, aver2, cov1, cov2):
    m = np.abs(aver1 - aver2) ** 2 / (cov1 + cov2)
    d = np.abs(cov1 + cov2) / (np.sqrt(np.abs(cov1 * cov2)) * 2)
    b = 0.125 * m + 0.5 * np.log(d)
    jm = 2 * (1 - np.exp(-1 * b))
    return jm


df1 = pd.read_csv('red_channel_terrain_classification.csv')
df1 = df1['mangrove']

df2 = pd.read_csv('/Users/ypk/PycharmProjects/mangrove/venv/lib/reflectance/Points-20-1.csv')
df2 = df2[df2['landcover'] == 0]
df2 = df2['red']

# 提取反射率数据
reflectance_mangrove = df1.values.reshape(-1, 1)
reflectance_check = df2.values.reshape(-1, 1)

# 计算均值向量
mean_mangrove = np.mean(reflectance_mangrove, axis=0)[0]
mean_check = np.mean(reflectance_check, axis=0)[0]

# 计算方差
cov_mangrove = np.cov(reflectance_mangrove, rowvar=False)
cov_check = np.cov(reflectance_check, rowvar=False)

# 计算 JM 距离
jm_distance = calculate_jm(mean_mangrove, mean_check, cov_mangrove, cov_check)

print(jm_distance)




