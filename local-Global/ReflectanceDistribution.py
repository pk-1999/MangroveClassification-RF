import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('GMD_v2.csv')

# Define the mapping of landcover values to their corresponding labels
landcover_labels = {
    1: 'mangrove',
    2: 'water',
    3: 'vegetation',
    4: 'plough',
    5: 'architecture',
    6: 'paddyfield',
    7: 'bare'
}
'''landcover_labels = {
    1: '红树林',
    2: '水体',
    3: '森林',
    4: '耕地及绿化',
    5: '建筑及道路',
    6: '水田及鱼塘',
    7: '裸地'
}'''

# Filter the DataFrame based on landcover values and calculate the value ranges for each channel
for landcover_value, landcover_label in landcover_labels.items():
    landcover_data = data[data['landcover'] == landcover_value]
    red_range = (landcover_data['red'].min(), landcover_data['red'].max())
    nir_range = (landcover_data['nir'].min(), landcover_data['nir'].max())
    swir1_range = (landcover_data['swir1'].min(), landcover_data['swir1'].max())
    swir2_range = (landcover_data['swir2'].min(), landcover_data['swir2'].max())
    '''
    print(f"Landcover: {landcover_label}")
    print(f"Red range: {red_range}")
    print(f"NIR range: {nir_range}")
    print(f"SWIR1 range: {swir1_range}")
    print(f"SWIR2 range: {swir2_range}")
    print()
    '''

# Create a boxplot for each channel
plt.rcParams["font.family"] = ['Times New Roman', 'Songti SC']

fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# Define the color control parameters
box_color = 'blue'  # Box color
median_color = 'green'  # Median color
mean_color = 'red'  # Mean color
flier_color = 'lightgray'  # Outlier point border color
flier_in_color = 'None'  # Outlier point fill color
patch_colors = ['yellow', 'white', 'white', 'white', 'white', 'white', 'white']  # Highlight mangrove


# Iterate over each channel
for i, channel in enumerate(['red', 'nir', 'swir1', 'swir2']):
    # Create a list to store the data for each landcover class
    landcover_data_list = []

    # Iterate over each landcover class
    for landcover_value, landcover_label in landcover_labels.items():
        # Filter the DataFrame based on landcover value and channel
        landcover_data = data[(data['landcover'] == landcover_value)][channel]
        landcover_data_list.append(landcover_data)

    # Plot the boxplot for each landcover class in the corresponding subplot
    boxplot = axs[i // 2, i % 2].boxplot(landcover_data_list, labels=landcover_labels.values(), showmeans=True,
                                    meanprops=dict(marker='x', markeredgecolor=mean_color),
                                    boxprops=dict(color=box_color),
                                    medianprops=dict(color=median_color),
                                    flierprops=dict(marker='o', markerfacecolor=flier_in_color,
                                                    markeredgecolor=flier_color),
                                    patch_artist=True)
    for patch, patch_color in zip(boxplot['boxes'], patch_colors):
        patch.set_facecolor(patch_color)

    axs[i // 2, i % 2].set_title(channel.upper())
    axs[i // 2, i % 2].set_xlabel('地物类别')
    axs[i // 2, i % 2].set_ylabel('反射率')

# Adjust the spacing between subplots
plt.tight_layout()

# Show the plot
plt.savefig("筛选前.png", dpi=300)
plt.show()