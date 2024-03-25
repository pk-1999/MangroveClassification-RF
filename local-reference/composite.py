import pandas as pd

# 文件路径
folder_path = ''  # 同文件夹下
# 定义起始和结束年份
start_year = 2019
end_year = 2023
# 定义季度列表
quarters = ['1', '2']
# 生成文件名列表
file_names = [f'{str(year)[-2:]}-{quarter}.csv' for year in range(start_year, end_year + 1) for quarter in quarters]

# 创建空数据框，用于存储所有年份的通道数据
data = pd.read_csv('19-1.csv')
reserved_column = ['system:index', 'landcover']
all_red_data = data[reserved_column]
all_green_data = data[reserved_column]
all_blue_data = data[reserved_column]
all_nir_data = data[reserved_column]
all_swir1_data = data[reserved_column]
all_swir2_data = data[reserved_column]

flag = True
# 循环处理每个文件
for file_name in file_names:
    df = pd.read_csv(file_name)

    # 提取各个通道的数据
    red_column = df[['system:index', 'red']]
    green_column = df[['system:index', 'green']]
    blue_column = df[['system:index', 'blue']]
    nir_column = df[['system:index', 'nir']]
    swir1_column = df[['system:index', 'swir1']]
    swir2_column = df[['system:index', 'swir2']]

    # 提取年份和季度信息
    year, temp_name = file_name.split('-')
    quarter, temp = temp_name.split('.')
    # 设置新的列名
    red_column_name = f'{year}-{quarter}_red'
    green_column_name = f'{year}-{quarter}_green'
    blue_column_name = f'{year}-{quarter}_blue'
    nir_column_name = f'{year}-{quarter}_nir'
    swir1_column_name = f'{year}-{quarter}_swir1'
    swir2_column_name = f'{year}-{quarter}_swir2'

    # 将各个通道的数据追加到相应的数据框中，并设置新的列名
    all_red_data = pd.merge(all_red_data, red_column.rename(columns={'system:index': 'system:index', 'red': red_column_name}), on='system:index')
    all_green_data = pd.merge(all_green_data, green_column.rename(columns={'system:index': 'system:index', 'green': green_column_name}), on='system:index')
    all_blue_data = pd.merge(all_blue_data, blue_column.rename(columns={'system:index': 'system:index', 'blue': blue_column_name}), on='system:index')
    all_nir_data = pd.merge(all_nir_data, nir_column.rename(columns={'system:index': 'system:index', 'nir': nir_column_name}), on='system:index')
    all_swir1_data = pd.merge(all_swir1_data, swir1_column.rename(columns={'system:index': 'system:index', 'swir1': swir1_column_name}), on='system:index')
    all_swir2_data = pd.merge(all_swir2_data, swir2_column.rename(columns={'system:index': 'system:index', 'swir2': swir2_column_name}), on='system:index')

# 写入各自的文件
all_red_data.to_csv('all_red_data.csv', index=False)
all_green_data.to_csv('all_green_data.csv', index=False)
all_blue_data.to_csv('all_blue_data.csv', index=False)
all_nir_data.to_csv('all_nir_data.csv', index=False)
all_swir1_data.to_csv('all_swir1_data.csv', index=False)
all_swir2_data.to_csv('all_swir2_data.csv', index=False)

print("Data from multiple years saved to individual files: all_red_data.csv, all_green_data.csv, all_blue_data.csv, all_nir_data.csv")
