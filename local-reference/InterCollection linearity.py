import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

# 读取CSV文件
data1 = pd.read_csv('S2L8-20-1.csv')
data2 = pd.read_csv('S2L8-20-2.csv')

# 使用rename方法进行格式化的重命名
data1.rename(columns=lambda x: x.replace('_L8_1', '_L8').replace('_S2_1', '_S2'), inplace=True)
data2.rename(columns=lambda x: x.replace('_L8_2', '_L8').replace('_S2_2', '_S2'), inplace=True)

# 打印结果
print(data1.columns)
print(data2.columns)

# 纵向合并两个DataFrame
data = pd.concat([data1, data2], axis=0)
print("Shape of the DataFrame:", data.shape)
print(data1.shape, '\t',  data2.shape)

# 获取不同landcover类别的数据
data_0 = data[data['landcover_S2'] == 0]
data_1 = data[data['landcover_S2'] == 1]

# 获取波段通道的列表
channels = ['red', 'green', 'blue', 'nir', 'swir1', 'swir2']
channel_names = ['Red', 'Green', 'Blue', 'NIR', 'SWIR1', 'SWIR2']

# 创建一个窗口，并设置子图的行和列
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10, 10.5))

# 循环绘制每种波段通道的散点图
for i in range(6):
    ax = axes.flat[i]
    channel = channels[i]
    channel_name = channel_names[i]
    x = data_0[f'{channel}_S2'].values.reshape(-1, 1)
    y = data_0[f'{channel}_L8'].values

    # 创建线性回归模型
    model = LinearRegression()
    model.fit(x, y)

    # 绘制散点图
    ax.scatter(x, y, label='Data', s=10)

    # 绘制拟合线
    ax.plot(x, model.predict(x), color='red', label='Linear Fit')

    # 添加线性拟合方程
    equation = f'y = {model.coef_[0]:.4f}x + {model.intercept_:.4f}'

    # 使用statsmodels计算R²
    X = sm.add_constant(x)
    results = sm.OLS(y, X).fit()
    r_squared = results.rsquared
    equation += f'\n$R^2$ = {r_squared:.4f}'

    # 添加方程和R²值到右下角
    ax.annotate(equation, xy=(0.95, 0.05), xycoords='axes fraction', fontsize=8, color='red', ha='right', va='bottom')

    ax.set_xlabel(f'{channel_name} channel of S2')
    ax.set_ylabel(f'{channel_name} channel of L8')
    ax.set_title(f'Relation Between {channel_name} Channel Of S2 And L8')
    ax.legend()

# 调整布局
plt.tight_layout()
# 导出图形
plt.savefig("S2L8不同通道反射率矫正.png", dpi=300)
# 显示图形
plt.show()
