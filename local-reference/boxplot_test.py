import matplotlib.pyplot as plt
import pandas as pd

# 读取各个通道的数据文件
red_df = pd.read_csv('all_red_data.csv')
green_df = pd.read_csv('all_green_data.csv')
blue_df = pd.read_csv('all_blue_data.csv')
nir_df = pd.read_csv('all_nir_data.csv')
swir1_df = pd.read_csv('all_swir1_data.csv')
swir2_df = pd.read_csv('all_swir2_data.csv')


def selectMangrove(df):
    return df[df['landcover'] == 1]


red_df = selectMangrove(red_df)
green_df = selectMangrove(green_df)
blue_df = selectMangrove(blue_df)
nir_df = selectMangrove(nir_df)
swir1_df = selectMangrove(swir1_df)
swir2_df = selectMangrove(swir2_df)

# 删除system:index和landcover列
columns_to_drop = ['system:index', 'landcover']

red_df = red_df.drop(columns=columns_to_drop, errors='ignore')  # 使用 errors='ignore' 避免在不存在的列时报错
green_df = green_df.drop(columns=columns_to_drop, errors='ignore')
blue_df = blue_df.drop(columns=columns_to_drop, errors='ignore')
nir_df = nir_df.drop(columns=columns_to_drop, errors='ignore')
swir1_df = swir1_df.drop(columns=columns_to_drop, errors='ignore')
swir2_df = swir2_df.drop(columns=columns_to_drop, errors='ignore')

#print(red_df.isnull().sum())
#print(red_df.describe())


# 创建一个包含4个子图的图形
plt.rcParams["font.family"] = "Times New Roman"
fig, axs = plt.subplots(2, 3, figsize=(15, 8))

# 定义颜色
box_color = 'blue' #箱
median_color = 'green'  #中值
mean_color = 'red'      #平均值
flier_color = 'lightgray'    #离群点边框
flier_in_color = 'None' #离群点内部填充

# 为每个通道绘制箱线图，并添加平均值点
axs[0, 0].boxplot(red_df.values, labels=red_df.columns.str[:4], showmeans=True, meanprops=dict(marker='x', markeredgecolor=mean_color), boxprops=dict(color=box_color), medianprops=dict(color=median_color), flierprops=dict(marker='o', markerfacecolor=flier_in_color, markeredgecolor=flier_color))
axs[0, 1].boxplot(green_df.values, labels=green_df.columns.str[:4], showmeans=True, meanprops=dict(marker='x', markeredgecolor=mean_color), boxprops=dict(color=box_color), medianprops=dict(color=median_color), flierprops=dict(marker='o', markerfacecolor=flier_in_color, markeredgecolor=flier_color))
axs[0, 2].boxplot(blue_df.values, labels=blue_df.columns.str[:4], showmeans=True, meanprops=dict(marker='x', markeredgecolor=mean_color), boxprops=dict(color=box_color), medianprops=dict(color=median_color), flierprops=dict(marker='o', markerfacecolor=flier_in_color, markeredgecolor=flier_color))
axs[1, 0].boxplot(nir_df.values, labels=nir_df.columns.str[:4], showmeans=True, meanprops=dict(marker='x', markeredgecolor=mean_color), boxprops=dict(color=box_color), medianprops=dict(color=median_color), flierprops=dict(marker='o', markerfacecolor=flier_in_color, markeredgecolor=flier_color))
axs[1, 1].boxplot(swir1_df.values, labels=swir1_df.columns.str[:4], showmeans=True, meanprops=dict(marker='x', markeredgecolor=mean_color), boxprops=dict(color=box_color), medianprops=dict(color=median_color), flierprops=dict(marker='o', markerfacecolor=flier_in_color, markeredgecolor=flier_color))
axs[1, 2].boxplot(swir2_df.values, labels=swir2_df.columns.str[:4], showmeans=True, meanprops=dict(marker='x', markeredgecolor=mean_color), boxprops=dict(color=box_color), medianprops=dict(color=median_color), flierprops=dict(marker='o', markerfacecolor=flier_in_color, markeredgecolor=flier_color))

# 调整坐标轴
upper_limit_1 = 0.5
upper_limit_2 = 0.65
upper_limit_3 = 0.65
axs[0, 0].set_ylim([0, upper_limit_1])
axs[0, 1].set_ylim([0, upper_limit_1])
axs[0, 2].set_ylim([0, upper_limit_1])
axs[1, 0].set_ylim([0, upper_limit_2])
axs[1, 1].set_ylim([0, upper_limit_3])
axs[1, 2].set_ylim([0, upper_limit_3])

# 添加标题和标签
fig.suptitle('Boxplots of Different Channel Values at Sample Points')
channels = ['Red', 'Green', 'Blue', 'NIR', 'SWIR1', 'SWIR2']
for i in range(6):
    ax = axs.flat[i]
    channel = channels[i]
    ax.set(xlabel='Time Index', ylabel=channel + ' Channel Values')

# 调整布局
plt.tight_layout()

# 导出图形
# plt.savefig("各通道年内变异性箱线图.png", dpi=300)
# 显示图形
plt.show()
