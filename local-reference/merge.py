import pandas as pd

# 读取两个CSV文件
file1 = pd.read_csv('L8-20-1.csv')
file2 = pd.read_csv('S2-20-1.csv')
file3 = pd.read_csv('L8-20-2.csv')
file4 = pd.read_csv('S2-20-2.csv')

# 合并具有相同标识字符串的点
merged_data1 = pd.merge(file1, file2, on='system:index')
merged_data2 = pd.merge(file3, file4, on='system:index')

# 提取合并后的数据中的通道信息
# channels = ['red_x', 'green_x', 'blue_x', 'nir_x', 'swir1_x', 'swir2_x', 'landcover_x', '.geo_x',
#            'red_y', 'green_y', 'blue_y', 'nir_y', 'swir1_y', 'swir2_y', 'landcover_y', '.geo_y']

# 重命名通道列，添加后缀以区分两个文件的通道
#merged_data.columns = ['system:index'] + [f'{channel[:-2]}_{suffix}' for channel in channels for suffix in ['x', 'y']]

# 保存合并后的数据到新文件
merged_data1.to_csv('S2L8-20-1.csv', index=False)
merged_data2.to_csv('S2L8-20-2.csv', index=False)
