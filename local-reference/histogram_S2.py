import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = 'S2-20-1.csv'
df = pd.read_csv(file_path)

# 获取不同landcover类别的数据
landcover_0 = df[df['landcover_S2_1'] == 0]
landcover_1 = df[df['landcover_S2_1'] == 1]

# 创建一个包含4个子图的画布
plt.figure(figsize=(15, 12))

# 定义颜色字典
colors = {0: 'red', 1: 'blue'}

# 定义全局变量 bins
bins = 100

# 循环绘制每种波段通道的直方图
for i, channel in enumerate(['red', 'green', 'blue', 'nir', 'swir1', 'swir2'], start=1):
    plt.subplot(2, 3, i)
    plt.hist(landcover_0[f'{channel}_S2_1'], bins=bins, alpha=0.5, color=colors[0], label='Landcover 0', density=True)
    plt.hist(landcover_1[f'{channel}_S2_1'], bins=bins, alpha=0.5, color=colors[1], label='Landcover 1', density=True)
    plt.title(f'{channel.capitalize()} Comparison')
    plt.xlabel(f'{channel.capitalize()} Values')
    plt.ylabel('Frequency (Percentage)')
    plt.legend()

# 调整子图之间的间距
plt.tight_layout()

# 显示图形
plt.show()
