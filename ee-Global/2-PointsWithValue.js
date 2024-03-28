var assetId = 'S2_Global';

var bands = ee.List(['red', 'nir', 'swir1', 'swir2']);
var classProperty = 'landcover';    //保留的属性

// ***********
// generate the ImageCollection available during this date range
var start = ee.Date.fromYMD(2019, 7, 1);
var end = ee.Date.fromYMD(2021, 1, 1);


// Make a cloud-free mask.
function maskS2sr(image) {
    image = ee.Image(image);
    // Band'QA60' Bits 10 and 11 are clouds and cirrus, respectively.
    var qa = image.select('QA60');
    var cloudBitMask = 1 << 10;
    var cirrusBitMask = 1 << 11;
    // Band'scl' has the classification flag
    var scl = image.select('SCL');
    var Cloud_Shadows = 1 << 3;
    var Clouds_Low_Probability = 1 << 7;
    var Clouds_Medium_Probability = 1 << 8;
    var Clouds_High_Probability = 1 << 9;
    var Cirrus = 1 << 10;
    var Snow_Ice = 1 << 11;
    // All flags should be set to zero, indicating clear conditions.
    var mask = scl.bitwiseAnd(Cloud_Shadows).eq(0)
        .and(scl.bitwiseAnd(Clouds_Low_Probability).eq(0))
        .and(scl.bitwiseAnd(Clouds_Medium_Probability).eq(0))
        .and(scl.bitwiseAnd(Clouds_High_Probability).eq(0))
        .and(scl.bitwiseAnd(Cirrus).eq(0))
        .and(scl.bitwiseAnd(Snow_Ice).eq(0))
        .and(qa.bitwiseAnd(cloudBitMask).eq(0))
        .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
    image = image.updateMask(mask);
    return image;
}
function addRefMean(image) {  // 识别删除去云错误影像
    image = ee.Image(image);
    var image_mean = image
        .select(['blue', 'green', 'red', 'nir'])
        .reduce(ee.Reducer.mean());
    var mean = image_mean
        .reduceRegion({
            reducer: ee.Reducer.mean(),
            scale: 120,
            geometry: image.geometry(),
            bestEffort: true
        });
    return image.set("ref_mean", mean.get('mean'));
}

// # Sentinel
var S2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterDate(start, end);

// Make a cloud-free mask
var Sentinel2 = S2.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    .map(maskS2sr)
    .select(['B2', 'B3', 'B4', 'B8A', 'B11', 'B12'], ['blue', 'green', 'red', 'nir', 'swir1', 'swir2']) //CAUTION! 
    .map(addRefMean)
    .filter(ee.Filter.lt("ref_mean", 1800))
    .select(bands)
    ;

function normalize(image) {
    image = ee.Image(image);
    // S2辐射定标 DN->反射率
    var RedBands = image.select(['red']).multiply(0.00018);
    var NIRBands = image.select(['nir']).multiply(0.00015);
    var SWIR1Bands = image.select('swir1').multiply(0.00014);
    var SWIR2Bands = image.select('swir2').multiply(0.00017);
    image = image.addBands(RedBands, null, true); // 保留属性！
    image = image.addBands(NIRBands, null, true);
    image = image.addBands(SWIR1Bands, null, true);
    image = image.addBands(SWIR2Bands, null, true);
    return image;
}

var S2 = Sentinel2.map(function (image) {
    return normalize(image).clamp(0, 1);
}).median();

var sample = S2.select(bands).sampleRegions({
    collection: samplePoints,   //采样范围，此处指从Points中的所有点
    properties: ['landcover'],  //保留的属性
    scale: 10,   //采样的空间分辨率,此处设置为30m
    geometries: true
});

Export.table.toAsset({
    collection: sample,
    description: 'samples',
    assetId: 'PointsWithValue/GMD_v1',
});
