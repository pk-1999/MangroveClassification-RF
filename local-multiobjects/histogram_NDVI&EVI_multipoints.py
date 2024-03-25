import matplotlib.pyplot as plt
import pandas as pd
from functools import reduce


def selectMangrove(df, flag):
    return df[df['landcover'] == flag]


# 读取CSV文件
df = pd.read_csv('/Users/ypk/PycharmProjects/mangrove/venv/lib/multiobjects/MultiPointsWithValue_first.csv')

channels = ['NDVI', 'EVI', 'NDWI', 'LSWI1', 'LSWI2', 'EMSI']
features = ['mangrove', 'water', 'vegetation', 'plough', 'architecture', 'paddyfield']

# 计算NDVI
df['NDVI'] = (df['nir'] - df['red']) / (df['nir'] + df['red'])

# 计算EVI
df['EVI'] = 2.5 * (df['nir'] - df['red']) / (df['nir'] + 6 * df['red'] - 7.5 * df['blue'] + 1)

# 计算NDWI
df['NDWI'] = (df['nir'] - df['green']) / (df['nir'] + df['green'])

# 计算LSWI
df['LSWI1'] = (df['nir'] - df['swir1']) / (df['nir'] + df['swir1'])
df['LSWI2'] = (df['nir'] - df['swir2']) / (df['nir'] + df['swir2'])

# 计算EMSI
df['EMSI'] = 2 * (df['nir'] + df['swir1']) * (df['swir1'] + df['swir2'])

# 获取不同landcover类别的数据
mangrove_df = selectMangrove(df, 1)
water_df = selectMangrove(df, 2)
vegetation_df = selectMangrove(df, 3)
plough_df = selectMangrove(df, 4)
architecture_df = selectMangrove(df, 5)
paddyfield_df = selectMangrove(df, 6)

# 创建一个包含6个子图的图形
plt.rcParams["font.family"] = "Times New Roman"
fig, axs = plt.subplots(3, 2, figsize=(10, 12))

# 定义横纵坐标
x_axis_label = 'Sample Points Feature Category'
y_axis_label_template = 'Reflectance Value'
channel_names = ['NDVI', 'EVI', 'NDWI', 'LSWI1', 'LSWI2', 'EMSI']

# 定义颜色
box_color = 'blue'  # 箱
median_color = 'green'  # 中值
mean_color = 'red'  # 平均值
flier_color = 'lightgray'  # 离群点边框
flier_in_color = 'None'  # 离群点内部填充
patch_colors = ['yellow', 'white', 'white', 'white', 'white', 'white']


def singleTerrain(df, channel, flag):
    df_channel = df[[channel]].rename(columns={channel: features[flag]})
    df_channel['index'] = range(1, len(df_channel) + 1)
    return df_channel


for i in range(3):
    for j in range(2):
        axs_index = 2 * i + j
        channel = channels[axs_index]
        print(channel)
        mangrove_df_channel = singleTerrain(mangrove_df, channel, 0)
        water_df_channel = singleTerrain(water_df, channel, 1)
        vegetation_df_channel = singleTerrain(vegetation_df, channel, 2)
        plough_df_channel = singleTerrain(plough_df, channel, 3)
        architecture_df_channel = singleTerrain(architecture_df, channel, 4)
        paddyfield_df_channel = singleTerrain(paddyfield_df, channel, 5)

        dfs = [mangrove_df_channel, water_df_channel, vegetation_df_channel, plough_df_channel,
               architecture_df_channel, paddyfield_df_channel]
        merged_df = reduce(lambda left, right: pd.merge(left, right, on='index'), dfs)
        merged_df = merged_df.drop(columns=['index'], errors='ignore')

        # 重排顺序
        new_order = ['mangrove', 'vegetation', 'plough', 'paddyfield', 'water', 'architecture']
        merged_df = merged_df[new_order]

        # 绘制
        boxplot = axs[i, j].boxplot(merged_df.values, labels=merged_df.columns, showmeans=True,
                                    meanprops=dict(marker='x', markeredgecolor=mean_color),
                                    boxprops=dict(color=box_color),
                                    medianprops=dict(color=median_color),
                                    flierprops=dict(marker='o', markerfacecolor=flier_in_color,
                                                    markeredgecolor=flier_color),
                                    patch_artist=True)

        for patch, patch_color in zip(boxplot['boxes'], patch_colors):
            patch.set_facecolor(patch_color)

        # Set labels and title
        channel_name = channel_names[axs_index]
        axs[i, j].set(xlabel=x_axis_label, ylabel=f'{channel_name} Channel {y_axis_label_template} ')
        axs[i, j].set_title(f'{channel_name} Channel Boxplot')

        # 导出csv
        # merged_df.to_csv(f'{channel}_channel_terrain_classification.csv')
        # print('successfully export')

# 调整坐标轴
upper_limit_1 = 0.8
upper_limit_2 = 1
upper_limit_3 = 1
axs[0, 0].set_ylim([-0.5, upper_limit_1])
axs[0, 1].set_ylim([-0.5, upper_limit_1])
axs[1, 0].set_ylim([-0.5, upper_limit_2])
axs[1, 1].set_ylim([-0.5, upper_limit_2])
axs[2, 0].set_ylim([-0.5, upper_limit_3])
axs[2, 1].set_ylim([-0.5, upper_limit_3])


# 添加标题和标签
fig.suptitle('Boxplots of Different Channel Values at Sample Points')

# 调整布局
plt.tight_layout()

# 导出图形
# plt.savefig("不同地物反射率箱线图.png", dpi=300)

# 显示图形
plt.show()
