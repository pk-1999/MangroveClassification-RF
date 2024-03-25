import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = 'Points-20-1.csv'
df = pd.read_csv(file_path)

# 计算NDVI
df['NDVI'] = (df['nir'] - df['red']) / (df['nir'] + df['red'])

# 计算EVI
df['EVI'] = 2.5 * (df['nir'] - df['red']) / (df['nir'] + 6 * df['red'] - 7.5 * df['blue'] + 1)

# 获取不同landcover类别的数据
landcover_0 = df[df['landcover'] == 0]
landcover_1 = df[df['landcover'] == 1]

# 创建一个包含2个子图的画布
plt.figure(figsize=(15, 6))

# 绘制第1个子图：NDVI的直方图
plt.subplot(1, 2, 1)
plt.hist(landcover_0['NDVI'], bins=100, alpha=0.5, color='green', label='Landcover 0', density=True)
plt.hist(landcover_1['NDVI'], bins=100, alpha=0.5, color='blue', label='Landcover 1', density=True)
plt.title('NDVI Comparison')
plt.xlabel('NDVI Values')
plt.ylabel('Frequency (Percentage)')
plt.legend()

# 绘制第2个子图：EVI的直方图
plt.subplot(1, 2, 2)
plt.hist(landcover_0['EVI'], bins=50, alpha=0.5, color='green', label='Landcover 0', density=True)
plt.hist(landcover_1['EVI'], bins=50, alpha=0.5, color='blue', label='Landcover 1', density=True)
plt.title('EVI Comparison')
plt.xlabel('EVI Values')
plt.ylabel('Frequency (Percentage)')
plt.legend()

# 调整子图之间的间距
plt.tight_layout()

# 显示图形
plt.show()
