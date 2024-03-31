import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import griddata

cv_results = np.load('n_estimators-min_samples_split-data_v1.npz')

print(cv_results.keys())

# 绘制3D图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  # '111'表示1行1列第一个位置

# 调整图像大小
fig.set_size_inches(10, 6)

param1 = 'n_estimators'
param2 = 'min_samples_split'
scores = cv_results['mean_test_score']

# Set the axes labels
ax.set_xlabel(param1)
ax.set_ylabel(param2)
ax.set_zlabel('Validation Accuracy')

param1_flag = np.array([100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500])
param2_flag = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10])
scores_2d = scores.reshape((17, 9))

# 创建平滑曲面
param1_smooth, param2_smooth = np.meshgrid(param1_flag, param2_flag)
scores_smooth = griddata((param1_smooth.ravel(), param2_smooth.ravel()), scores.ravel(), (param1_smooth, param2_smooth), method='cubic')

# 绘制平滑曲面
surf = ax.plot_surface(param1_smooth, param2_smooth, scores_smooth, cmap='viridis')

# 添加颜色条
cbar = fig.colorbar(surf, shrink=0.5, aspect=15)    # shrink参数表示缩小比例，aspect参数表示颜色条的宽度
cbar.ax.set_position([0.8, 0.2, 0.02, 0.5])  # 设置颜色条的位置和大小
# cbar.set_label('Validation Accuracy')

# 设置初始角度
ax.view_init(elev=25, azim=127, roll=0)

# 保存图像为PNG格式
plt.savefig('grid_search_result.png', dpi=300, bbox_inches='tight') # bbox_inches='tight'表示紧凑显示图像

# 显示图像
plt.title('参数寻优结果')
plt.show()
