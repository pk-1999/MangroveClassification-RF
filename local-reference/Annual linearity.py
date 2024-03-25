import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

# 读取CSV文件
data = pd.read_csv('S2-20.csv')

# 获取波段通道的列表
channels = ['blue', 'green', 'nir', 'red', 'swir1', 'swir2']

# 创建一个窗口，并设置子图的行和列
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 6))

# 循环绘制每种波段通道的散点图
for ax, channel in zip(axes.flat, channels):
    x = data[f'{channel}_S2_1'].values.reshape(-1, 1)
    y = data[f'{channel}_S2_2'].values

    # 创建线性回归模型
    model = LinearRegression()
    model.fit(x, y)

    # 绘制散点图
    ax.scatter(x, y, label='Data')

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

    ax.set_xlabel(f'{channel}_S2_1')
    ax.set_ylabel(f'{channel}_S2_2')
    ax.set_title(f'Relation between {channel}_S2_1 and {channel}_S2_2')
    ax.legend()

# 调整布局
plt.tight_layout()

# 显示图形
plt.show()
