import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def normalize(data):
    min_val = np.min(data)
    max_val = np.max(data)
    normalized_data = 2 * (data - min_val) / (max_val - min_val) - 1
    return normalized_data



# 读取CSV文件
file_path = 'Points-20-1.csv'
df = pd.read_csv(file_path)

# 计算NDVI
df['NDVI'] = (df['nir'] - df['red']) / (df['nir'] + df['red'])

# 计算NDWI
df['NDWI'] = (df['nir'] - df['green']) / (df['nir'] + df['green'])

# 计算LSWI
df['LSWI1'] = (df['nir'] - df['swir1']) / (df['nir'] + df['swir1'])
df['LSWI2'] = (df['nir'] - df['swir2']) / (df['nir'] + df['swir2'])

# 计算EMSI
df['EMSI'] = df['NDVI'] * (df['swir1'] - df['swir2']) / (df['swir1'] + df['swir2'])

# 计算MVI
df['MVI1'] = (df['nir'] - df['green']) / (df['swir1'] - df['green'])
df['MVI2'] = (df['nir'] - df['green']) / (df['swir2'] - df['green'])

# 手搓！
df['new'] = (df['MVI1'] - df['EMSI']) / (df['MVI2'] - df['EMSI'])

df['NDVI'] = normalize(df['NDVI'])
df['NDWI'] = normalize(df['NDWI'])
df['LSWI1'] = normalize(df['LSWI1'])
df['LSWI2'] = normalize(df['LSWI2'])
df['new'] = normalize(df['new'])

# 获取不同landcover类别的数据
landcover_0 = df[df['landcover'] == 0]
landcover_1 = df[df['landcover'] != 0]

# 创建一个包含2个子图的画布
plt.figure(figsize=(15, 10))

# 绘制第1个子图
plt.subplot(2, 2, 1)
plt.hist(landcover_1['LSWI1'], bins=60, alpha=0.5, color='blue', label='Mangrove', density=True)
plt.hist(landcover_0['LSWI1'], bins=60, alpha=0.5, color='green', label='Others', density=True)
plt.title('LSWI1 Comparison')
plt.xlabel('LSWI1 Values')
plt.ylabel('Frequency (Percentage)')
plt.legend()

# 绘制第2个子图
plt.subplot(2, 2, 2)
plt.hist(landcover_1['LSWI2'], bins=60, alpha=0.5, color='blue', label='Mangrove', density=True)
plt.hist(landcover_0['LSWI2'], bins=60, alpha=0.5, color='green', label='Others', density=True)
plt.title('LSWI2 Comparison')
plt.xlabel('LSWI2 Values')
plt.ylabel('Frequency (Percentage)')
plt.legend()

# 绘制第3个子图
plt.subplot(2, 2, 3)
plt.hist(landcover_1['NDWI'], bins=60, alpha=0.5, color='blue', label='Mangrove', density=True)
plt.hist(landcover_0['NDWI'], bins=60, alpha=0.5, color='green', label='Others', density=True)
plt.title('NDWI Comparison')
plt.xlabel('NDWI Values')
plt.ylabel('Frequency (Percentage)')
plt.legend()

# 绘制第4个子图
plt.subplot(2, 2, 4)
plt.hist(landcover_1['EMSI'], bins=60, alpha=0.5, color='blue', label='Mangrove', density=True)
plt.hist(landcover_0['EMSI'], bins=60, alpha=0.5, color='green', label='Others', density=True)
plt.title('new Comparison')
plt.xlabel('new Values')
plt.ylabel('Frequency (Percentage)')
plt.legend()

# 调整子图之间的间距
plt.tight_layout()

# 显示图形
plt.show()
