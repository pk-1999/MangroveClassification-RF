import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = 'Points-20-1.csv'
df = pd.read_csv(file_path)

# 获取不同landcover类别的数据
landcover_0 = df[df['landcover'] == 0]
landcover_1 = df[df['landcover'] == 1]

# 创建一个包含4个子图的画布
plt.figure(figsize=(15, 12))

# 绘制第1个子图：landcover=0和landcover=1的red通道直方图
plt.subplot(2, 2, 1)
plt.hist(landcover_0['red'], bins=100, alpha=0.5, color='red', label='Landcover 0', density=True)
plt.hist(landcover_1['red'], bins=100, alpha=0.5, color='blue', label='Landcover 1', density=True)
plt.title('Red Comparison')
plt.xlabel('Red Values')
plt.ylabel('Frequency (Percentage)')
plt.legend()

# 绘制第2个子图：landcover=0和landcover=1的green通道直方图
plt.subplot(2, 2, 2)
plt.hist(landcover_0['green'], bins=100, alpha=0.5, color='green', label='Landcover 0', density=True)
plt.hist(landcover_1['green'], bins=100, alpha=0.5, color='purple', label='Landcover 1', density=True)
plt.title('Green Comparison')
plt.xlabel('Green Values')
plt.ylabel('Frequency (Percentage)')
plt.legend()

# 绘制第3个子图：landcover=0和landcover=1的blue通道直方图
plt.subplot(2, 2, 3)
plt.hist(landcover_0['blue'], bins=100, alpha=0.5, color='blue', label='Landcover 0', density=True)
plt.hist(landcover_1['blue'], bins=100, alpha=0.5, color='cyan', label='Landcover 1', density=True)
plt.title('Blue Comparison')
plt.xlabel('Blue Values')
plt.ylabel('Frequency (Percentage)')
plt.legend()

# 绘制第4个子图：landcover=0和landcover=1的nir通道直方图
plt.subplot(2, 2, 4)
plt.hist(landcover_0['nir'], bins=100, alpha=0.5, color='green', label='Landcover 0', density=True)
plt.hist(landcover_1['nir'], bins=100, alpha=0.5, color='yellow', label='Landcover 1', density=True)
plt.title('NIR Comparison')
plt.xlabel('NIR Values')
plt.ylabel('Frequency (Percentage)')
plt.legend()

# 调整子图之间的间距
plt.tight_layout()

# 显示图形
plt.show()
