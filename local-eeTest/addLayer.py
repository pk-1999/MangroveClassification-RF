import ee
import folium
from IPython.display import Image

# 初始化 Earth Engine
ee.Authenticate()
ee.Initialize(project='ee-pkyu1999')

# 选择一个地点的坐标
location = ee.Geometry.Point(-122.4394, 37.7749)

# 在地图上显示该地点
map_center = [location.getInfo()['coordinates'][1], location.getInfo()['coordinates'][0]]
mymap = folium.Map(location=map_center, zoom_start=12)

# 在地图上添加一个 EE 图像
landsat_image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')
landsat_vis_params = {'bands': ['B4', 'B3', 'B2'], 'min': 6000, 'max': 12000, 'gamma': 1.4}
folium.TileLayer(
    tiles=landsat_image.getMapId(landsat_vis_params),
    attr='Google Earth Engine',
    overlay=True,
    name='landsat_image',
).add_to(mymap)

# 添加一个 EE 图层（这里示范添加一些点）
points = ee.FeatureCollection([
    ee.Feature(location, {'name': 'Selected Location'})
])
folium.GeoJson(data=points.geometry().getInfo(), name='Points').add_to(mymap)

# 显示地图
mymap
