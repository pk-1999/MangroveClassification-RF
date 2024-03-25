import folium
import geemap as emap
import ee

# Initialize the Earth Engine library.
ee.Authenticate()
ee.Initialize(project='ee-pkyu1999')

# 定义感兴趣区域
haLongRegion = ee.Geometry.Rectangle([106.5, 20.52, 107.04, 21.02])

# 加载红树林全球分布数据集
MangroveDistribution = ee.FeatureCollection("projects/ee-pkyu1999/assets/mangrove/LREIS_GLOBALMANGROVE_v2_shp_10m")

# 进行空间过滤
filteredCollection = MangroveDistribution.filterBounds(haLongRegion)

# 对要素进行缓冲区操作
bufferedCollection = filteredCollection.map(lambda feature: feature.buffer(1000))

# 创建地图
m = folium.Map(location=[21, 107], zoom_start=10)

# 将 Earth Engine 数据添加到地图
ee_map = emap.Map()
ee_map.centerObject(haLongRegion, 5)
ee_map.addLayer(filteredCollection, {'color': 'orange', 'max': 1, 'opacity': 0.7}, 'Mangrove Distribution')
ee_map.addLayer(bufferedCollection, {'color': 'green', 'max': 1, 'opacity': 0.5}, 'Buffered Mangrove Distribution')

# 将 ee.Map 转为 folium.Map，并添加到最终的地图
folium_map = folium.Map(location=[21, 107], zoom_start=10)
folium_map.add_child(ee_map)

# 在本地显示地图
folium_map.save("mangrove_map.html")
