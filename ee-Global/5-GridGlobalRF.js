var elevation = ee.Image("USGS/SRTMGL1_003"),
    SamplePoints = ee.FeatureCollection("projects/ee-pkyu1999/assets/PointsWithValue/GMD_v2_cleansed");

var longitude_list = ee.List.sequence(0, 350, 10);
var latitude_list = ee.List.sequence(-30, 10, 20);

var roi_list = longitude_list.map(function (longitude_start) {
    longitude_start = ee.Number(longitude_start);
    var roi_column = latitude_list.map(function (latitude_start) {
        latitude_start = ee.Number(latitude_start);
        return ee.Geometry.Rectangle([longitude_start, latitude_start, longitude_start.add(10), latitude_start.add(20)]);
    });
    return roi_column;
}).flatten();

//var saveIndex = ee.List([1, 3, 4, 9, 10, 11, 12, 13, 14, 17, 20, 22, 23, 25, 26, 28, 29, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 48, 49, 51, 62, 74, 77, 80, 82, 83, 84, 85, 86, 88, 89, 91, 93, 94, 96, 97, 103, 104, 106]);
var saveIndex = ee.List([1, 3, 4, 9, 10]);

// **********************************

var startYear = ee.Number(2019);
var endYear = ee.Number(2019);

//var name_image = ee.List(['19-1', '19-2', '20-1', '20-2', '21-1', '21-2', '22-1', '22-2', '23-1', '23-2']);
var name_image = ee.List(['19-1', '19-2']);

var count_grid = 53;
var count_time = 2;
var folder = 'Global';
var assetId = 'classified';

var bands = ee.List(['red', 'nir', 'swir1', 'swir2']);
var classProperty = 'landcover';    //保留的属性

var filterRadius = 50;

// ***********
// generate the Image available during this date range
var start = ee.Date.fromYMD(startYear, 1, 1);
var end = ee.Date.fromYMD(endYear.add(1), 1, 1);

var yearList = ee.List.sequence(startYear, endYear, 1);
var dateList = ee.List([[[1, 1], [6, 30]], [[7, 1], [12, 31]]]);


// *********
// RF
var classProperty = 'landcover';

var withRandom = SamplePoints.randomColumn({ seed: 123 });
var split = 0.8;
var trainingPartition = withRandom.filter(ee.Filter.lt('random', split));
var testingPartition = withRandom.filter(ee.Filter.gte('random', split));

var trainedClassifier = ee.Classifier.smileRandomForest(250).train({
    features: trainingPartition,
    classProperty: classProperty,
    inputProperties: bands
});

// *************
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
function addRefMean(image, roi) {  // 识别删除去云错误影像
    image = ee.Image(image);
    var image_mean = image
        .select(['blue', 'green', 'red', 'nir'])
        .reduce(ee.Reducer.mean());
    var mean = image_mean
        .reduceRegion({
            reducer: ee.Reducer.mean(),
            scale: 120,
            geometry: roi,
            bestEffort: true
        });
    return image.set("ref_mean", mean.get('mean'));
}
var elevationMask = elevation.lt(8);
function normalize(image) {
    image = ee.Image(image);
    // S2辐射定标 DN->反射率
    var RedBands = image.select(['red']).multiply(0.00018);
    var NIRBands = image.select(['nir']).multiply(0.00015);
    var SWIR1Bands = image.select(['swir1']).multiply(0.00014);
    var SWIR2Bands = image.select(['swir2']).multiply(0.00017);
    image = image.addBands(RedBands, null, true); // 保留属性！
    image = image.addBands(NIRBands, null, true);
    image = image.addBands(SWIR1Bands, null, true);
    image = image.addBands(SWIR2Bands, null, true);
    return image;
}

var S2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterDate(start, end);


// ***************
var outputImages_list_list = saveIndex.map(function (theIndex) {
    var roi = ee.Geometry(roi_list.get(theIndex));
    // Make a cloud-free mask
    var Sentinel2 = ee.ImageCollection(S2)
        .filterBounds(roi)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        .map(function (image) {
            image = image.updateMask(elevationMask);
            return image.clip(roi);
        })
        .map(maskS2sr)
        .select(['B2', 'B3', 'B4', 'B8A', 'B11', 'B12'], ['blue', 'green', 'red', 'nir', 'swir1', 'swir2']) //CAUTION! 
        .map(function (image) {
            image = ee.Image(image);
            return addRefMean(image, roi);
        })
        .filter(ee.Filter.lt("ref_mean", 1800))
        .select(bands)
        ;

    // 时间序列影像合成为Image
    var S2_imageList = yearList.map(function (year) {
        year = ee.Number(year);
        return dateList.map(function (days) {
            days = ee.List(days);
            var date_1 = ee.List(days.get(0));
            var date_2 = ee.List(days.get(1));
            var date_begin = ee.Date.fromYMD(year, date_1.get(0), date_1.get(1));
            var date_end = ee.Date.fromYMD(year, date_2.get(0), date_2.get(1)).advance(1, 'day');
            var images = Sentinel2
                .filterDate(date_begin, date_end)
                .median()
                .clip(roi);
            return images;
        });
    }).flatten();
    S2_imageList = S2_imageList.map(function (image) {
        return normalize(image).clamp(0, 1);
    });


    // RF
    var img_Region = ee.Image.constant(1).updateMask(elevationMask).clip(roi).rename('landcover');
    var classified = S2_imageList.map(function (image) {
        image = ee.Image(image);
        var restrictedImage = image.classify(trainedClassifier).updateMask(img_Region);   //.updateMask(img_BMD)
        var landcoverImage_multi = restrictedImage.rename(['landcover']);
        var zeroMaskedImage = ee.Image(0).clip(image.geometry()).rename(['landcover']);
        var landcoverImage = zeroMaskedImage.where(landcoverImage_multi.updateMask(landcoverImage_multi.eq(1)), landcoverImage_multi);
        var compositeImage = zeroMaskedImage.where(img_Region, landcoverImage);
        // 应用中值滤波
        var filteredImage = compositeImage.reduceNeighborhood({
            reducer: ee.Reducer.mode(),  // 选择中值滤波
            kernel: ee.Kernel.square({ radius: filterRadius, units: 'meters' }),  // 定义滤波器半径
        });
        return filteredImage.copyProperties(image, image.propertyNames());//.rename(['landcover']);
    });

    return ee.List(classified);
});

// var outputImages = ee.ImageCollection.fromImages(classified);


//******************
// output
for (var i = 0; i < count_grid; i++) {
    var outputImages_list = ee.List(outputImages_list_list.get(i));
    var f_name_grid = i;
    var j = 0;
    var f_name_time = name_image.get(j).getInfo();
    var toAssetImage = ee.Image(outputImages_list.get(i));
    // 导出
    Export.image.toAsset({
        image: toAssetImage,
        assetId: folder + '/' + assetId + '/' + f_name_grid + '-' + f_name_time,
        description: assetId + f_name_grid + '-' + f_name_time + 'classified',
        region: toAssetImage.geometry(),
        scale: 10, //重采样使空间分辨率为30m
        crs: "EPSG:4326", //使用WGS84坐标系
        maxPixels: 1e13,
        pyramidingPolicy: {  // 设置金字塔模式
            '.default': 'mode'
        }
    });
}

