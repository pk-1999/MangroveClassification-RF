var GMD_GM2020 = ee.FeatureCollection("projects/ee-pkyu1999/assets/mangrove/GlobalMangrove2020"),
    elevation = ee.Image("USGS/SRTMGL1_003");

var S2_and_L8 = ee.Image("projects/ee-pkyu1999/assets/S2_and_L8-China/20-1");
var roi = /* color: #98ff00 */ee.Geometry.Polygon(
    [[[108.01757161486313, 21.789945512875757],
    [108.08363833745882, 21.34770620566116],
    [108.51635439607479, 21.535693709858617],
    [109.35317186544138, 21.37864551830771],
    [109.67482733991957, 20.2279164228556],
    [108.2900142380906, 19.66982471756799],
    [108.356182278942, 18.2979758301751],
    [109.8729666340648, 17.859348973082557],
    [110.68757292314653, 18.724516213443103],
    [111.36753725373032, 19.711564567695774],
    [110.75194195132914, 20.55770764714599],
    [110.83979858948815, 21.276410131476887],
    [112.20273623046478, 21.578366294290603],
    [112.81828006354702, 21.440334963513248],
    [114.29863100729894, 21.927495176509336],
    [114.75280617484212, 22.439552302951395],
    [116.64346868135688, 22.819968238568947],
    [117.35258204352684, 23.328128452843824],
    [117.94057876968616, 23.914735847396134],
    [119.32573655185612, 25.08495623286363],
    [119.52910119200689, 25.084903568909144],
    [119.76154423652069, 25.33720505567478],
    [120.85563553803182, 24.82083365970125],
    [120.19511834269353, 23.92111024715092],
    [120.0863096154855, 23.614750685122],
    [120.10297007296319, 23.406226509098023],
    [120.05374661827565, 23.338814891771523],
    [120.03170834493515, 23.17090784170798],
    [119.99573904862919, 23.0771400778596],
    [120.20288012335597, 22.719188258646238],
    [120.31112204504048, 22.479189802512735],
    [120.53790167519507, 22.354038514165186],
    [120.63733811802372, 22.19470587219679],
    [120.70897834016928, 21.893821594392648],
    [120.90117313379078, 21.878119328690907],
    [120.91631851983357, 22.04820530464138],
    [120.9369942922568, 22.172462665184334],
    [120.98012158930925, 22.44538903580176],
    [121.08115301978434, 22.64714663993257],
    [121.36952046152973, 22.94650431655916],
    [121.56648045198007, 23.530968135072467],
    [121.68241425465656, 24.100166063484384],
    [121.88108533848037, 24.39424307905964],
    [121.92873258275164, 24.622490110013395],
    [121.8995091676782, 24.850736580005915],
    [122.09637238463309, 25.07400566805607],
    [121.76864754538175, 25.219064589130962],
    [121.57205615229493, 25.368501057524387],
    [121.34794566963065, 25.199998213543434],
    [121.0502777649571, 25.098213752030507],
    [120.8733183159952, 24.85198200079383],
    [119.78687741778799, 25.35817634375017],
    [119.92717373732154, 25.499669010035312],
    [120.02384785221045, 25.690650032300137],
    [119.78225906083513, 25.848904527868132],
    [119.82603109720648, 26.11091462836655],
    [120.04978078139479, 26.25820046948146],
    [120.08155409779587, 26.425092877307765],
    [120.41545490538736, 26.679606339592915],
    [120.42433524068217, 26.859489074979628],
    [120.85412710400529, 27.645328473551842],
    [120.38236937213591, 27.732808328507325],
    [119.90952528556595, 27.074014087297883],
    [119.59588559567685, 27.044897334890948],
    [119.33783154193239, 26.81935635416351],
    [119.21682600199351, 25.80930573917994],
    [117.32594395010199, 24.390936042775802],
    [115.87086908874119, 23.27594658850731],
    [114.9543635091325, 23.179732165670035],
    [114.10663059507294, 22.896739276401252],
    [113.2382338742185, 23.46763465799423],
    [112.92716146135481, 23.240507015850987],
    [112.69410682108052, 22.932121894624704],
    [112.85357173289911, 22.282719964679778],
    [112.089646417346, 22.130028839090166],
    [110.52336382460481, 21.640322342314597],
    [109.89628031925778, 21.671931300188866],
    [109.3851298361538, 21.927014344484466],
    [108.48122660857003, 22.022960765318356]]]);

// ***********
// 随机取样控制
var scale = 10;
var numPixels = 10000;
var seed = 222;
var extraSeed = 6;

// output
var assetID = 'RMD_GM2020_ZhanJiang';
var GMD = GMD_GM2020;
var RMD = GMD.filterBounds(roi);
// Map.centerObject(roi, 9);

Map.addLayer(S2_and_L8, { band: ['red', 'green', 'blue'], min: 0, max: 0.25 }, 'S2_and_L8', false);

// 定义中值滤波的半径
var filterRadius = 50;

// *******************

// 将 filteredCollection 中的要素进行缓冲
var BMD = RMD.map(function (feature) {
    return feature.buffer(2000);
});

// 在 RMD 中设置 'value' 属性为 1
RMD = RMD.map(function (feature) {
    return feature.set('value', 1);
});
// 在 BMD 中设置 'value' 属性为 0
BMD = BMD.map(function (feature) {
    return feature.set('value', 0);
});

// 将 FeatureCollection 转换为 Image
var img_RMD = RMD.reduceToImage(['value'], ee.Reducer.first()).eq(1);
var img_BMD = BMD.reduceToImage(['value'], ee.Reducer.first()).eq(0);
var elevationMask = elevation.lt(10);//.and(elevation.gt(-4));
var img_Region = ee.Image.constant(1).updateMask(img_BMD.and(elevationMask)).clip(roi).rename('landcover');
//Map.addLayer(elevationMask, {min: -10, max: 10, palette: ['white', 'black']}, 'Elevation Image');
Map.addLayer(img_Region, { min: 0, max: 1, palette: ['white', 'grey'] }, 'Interest region Image', false);


// *******************
// 随机取样 
// 生成种子值序列
var seeds = ee.List.sequence(seed + 1, seed + extraSeed);
var sampledPointsList = seeds.map(function (seedValue) {
    return img_RMD.sample({
        region: roi,
        scale: scale,
        numPixels: numPixels,
        seed: seedValue,
        geometries: true
    });
});
// 通过 flatten 函数一次性合并所有采样点
var points_RMD_extend = ee.FeatureCollection(sampledPointsList).flatten();
// 设置 'landcover' 属性为 1
points_RMD_extend = points_RMD_extend.map(function (feature) {
    return feature.set('landcover', 1);
});

var points_RMD = img_RMD.sample({
    region: roi,
    scale: scale,
    numPixels: numPixels,
    seed: seed,
    geometries: true
});
points_RMD = points_RMD.map(function (feature) {
    return feature.set('landcover', 1);   // 在随机点集中设置 'landcover' 属性为 1
});

var points_BMD = img_BMD.sample({
    region: roi,
    scale: scale,
    numPixels: numPixels,
    seed: seed,
    geometries: true
});
points_BMD = points_BMD.map(function (feature) {
    return feature.set('landcover', 0);   // 在第二个随机点集中设置 'landcover' 属性为 0
});

// 获取每个元素的 'id' 值
var pointsIds_RMD = points_RMD.toList(points_RMD.size()).map(function (feature) {
    return ee.Feature(feature).get('system:index');
});

// 对 points_BMD 集合进行映射，如果 'id' 在 PointsIds 中，则修改 'value' 为 1
var updatedPoints_BMD = points_BMD.map(function (feature) {
    var index = feature.get('system:index');
    var shouldUpdate = pointsIds_RMD.contains(index);
    return feature.set('landcover', ee.Algorithms.If(shouldUpdate, 1, 0));
});

updatedPoints_BMD = updatedPoints_BMD.merge(points_RMD_extend);

// 打印结果
print('Is_mangrove: ', updatedPoints_BMD.filter(ee.Filter.eq('landcover', 1)).size());
print('Not_mangrove: ', updatedPoints_BMD.filter(ee.Filter.eq('landcover', 0)).size());

// *******************
// RF 
var newfc = updatedPoints_BMD;
// var newfc = ee.FeatureCollection("projects/ee-pkyu1999/assets/mangrove/RMD_LREIS_roi");

var bands = ['blue', 'green', 'red', 'nir'];
var classProperty = 'landcover';

var training = S2_and_L8.select(bands).sampleRegions({
    collection: newfc,   //采样范围，此处指从newfc中的所有点
    properties: [classProperty],  //保留的属性
    scale: scale,   //采样的空间分辨率,此处设置为30m
    geometries: true
});

var withRandom = training.randomColumn('random');
var split = 0.7;
var trainingPartition = withRandom.filter(ee.Filter.lt('random', split));
var testingPartition = withRandom.filter(ee.Filter.gte('random', split));
print(testingPartition);
// Export!
Export.table.toAsset({
    collection: withRandom,
    assetId: assetID,
    description: 'sample_points',
});

var trainedClassifier = ee.Classifier.smileRandomForest(200).train({
    features: trainingPartition,
    classProperty: classProperty,
    inputProperties: bands
});

var test = testingPartition.classify(trainedClassifier);
var confusionMatrix = test.errorMatrix(classProperty, 'classification');
print('Confusion Matrix', confusionMatrix);
print('kappa', confusionMatrix.kappa());

var classified = S2_and_L8.classify(trainedClassifier).updateMask(img_Region);   //.updateMask(img_BMD)
Map.addLayer(classified, { min: 0, max: 1, palette: ['red', 'blue'] }, 'prediction');
Map.addLayer(roi, { color: 'white', opacity: 0.001 }, 'interest region', false);

// **********
// 应用中值滤波
var filteredImage = classified.reduceNeighborhood({
    reducer: ee.Reducer.mode(),  // 选择中值滤波
    kernel: ee.Kernel.square({ radius: filterRadius, units: 'meters' }),  // 定义滤波器半径
});

// 可视化分类后处理结果
Map.addLayer(filteredImage.updateMask(filteredImage.neq(0)), { min: 0, max: 1, palette: ['red', 'blue'] }, 'Filtered Classification');
Map.addLayer(GMD_GM2020, { color: 'yellow', opacity: 0.3 }, 'GMD_GM2020', false);
