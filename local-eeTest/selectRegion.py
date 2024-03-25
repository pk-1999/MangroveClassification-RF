import ee
import geemap

# filter to region
def filterToRegion(Region, GMDdatabase):
    RMDdatabase = []
    for GMD in GMDdatabase:
        RMD = GMD.filterBounds(Region)
        RMDdatabase.append(RMD)
    return RMDdatabase

def toImage(RMDdatabase):
    i = 0
    RMDimage = []
    for RMD in RMDdatabase:
        Img = RMD.map(lambda feature: feature.set('landcover', 1)).reduceToImage(['landcover'], ee.Reducer.first())
        RMDimage.append(Img)
        i += 1
    print("complete " + str(i) + "convert actions")
    return RMDimage

# generate a buffered FeatureCollection
def mask(RMD):
    BMD = RMD.map(lambda feature: feature.buffer(500))
    BMD = BMD.map(lambda feature: feature.set('landcover', 1))  #将距离红树林小于500m的位置设为1
    Img = BMD.reduceToImage(['landcover'], ee.Reducer.first())
    Mask = Img.eq(1)
    return Mask


# 初始化 Earth Engine
ee.Authenticate()
ee.Initialize(project='ee-pkyu1999')

# 定义感兴趣区域
haLongRegion = ee.Geometry.Rectangle([106.9, 20.9, 107.0, 21.0])

# 加载红树林全球分布数据集，并记录至列表
GMD_LREIS = ee.FeatureCollection("projects/ee-pkyu1999/assets/mangrove/LREIS_GLOBALMANGROVE_v2_shp_10m")
GMDdatabase = [GMD_LREIS]

# 对所有数据集进行空间过滤
RMDdatabase = filterToRegion(haLongRegion, GMDdatabase)
RMGimage = toImage(RMDdatabase)

# 对要素进行缓冲区操作，并生成遮罩
Mask = mask(RMDdatabase[0])

# 可视化
Map = geemap.Map()
Map.centerObject(haLongRegion, 12)
for Image in RMGimage:
    Map.addLayer(Image, {'min': 0, 'max': 1, 'palette': ['white', 'blue'], 'opacity': 0.3}, 'Rasterized Image')
Map.addLayerControl()
Map


# 判断每个点是否在红树林区域内
def checkMangrove(feature, RMGimage):
    point = ee.Feature(feature.geometry())
    i = 0
    sum = 0.0
    for img in RMGimage:
        sum += img.sample(point).get('landcover')
        i += 1
    is_mangrove = ee.Algorithms.If(ee.Algorithms.If(sum, sum > 0.5*i, 0), 1, 0)
    return feature.set('landcover', is_mangrove)


# 随机取样100个点
random_points = mask.sample(**{
    'region': haLongRegion,
    'scale': 30,
    'numPixels': 100,
    'seed': 1,
    'geometries': True
})

# 将随机点根据是否在红树林区域内分别添加到 FeatureCollection
mangrove = random_points.map(lambda feature: checkMangrove(feature, RMGimage))
print(mangrove.getInfo())

# 可视化
Map.addLayer(random_points, {'color': 'red'}, 'Random Points')
Map.addLayer(mangrove, {'color': 'green'}, 'Mangrove Samples')

Map
