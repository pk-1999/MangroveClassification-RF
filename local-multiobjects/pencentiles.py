import pandas as pd
import numpy as np

channels = ['red', 'nir', 'swir1', 'swir2']

matrix = np.zeros((4, 6))

for i in range(4):
    channel = channels[i]
    file_path = channel + '_channel_terrain_classification.csv'
    data = pd.read_csv(file_path)
    data = data[['mangrove', 'vegetation', 'plough', 'paddyfield', 'water', 'architecture']]

    # 计算每列的分位数
    percentiles = [0.15, 0.50, 0.85]
    result = data.describe(percentiles=percentiles)

    # 选择所需的行并转换为NumPy数组
    row_values = result.loc['85%'].values
    matrix[i, :] = row_values

# 打印结果
print(matrix)
