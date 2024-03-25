function CreateRoi() {
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
    return roi;
}
var roi = CreateRoi();

var startYear = ee.Number(2019);
var endYear = ee.Number(2023);

var name_image = ee.List(['19-1', '19-2', '20-1', '20-2', '21-1', '21-2', '22-1', '22-2', '23-1', '23-2']);

var count = 10;
//var folder = 'image_China';
var assetId = 'S2_and_L8-China_v3';

var bands = ee.List(['blue', 'green', 'red', 'nir', 'swir1', 'swir2']);
var classProperty = 'landcover';    //保留的属性

// ***********
// generate the ImageCollection available during this date range
var start = ee.Date.fromYMD(startYear, 1, 1);
var end = ee.Date.fromYMD(endYear.add(1), 1, 1);

// # Landsat
//var L9 = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2").filterDate(start, end).filterBounds(roi);
var L8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").filterDate(start, end).filterBounds(roi);
//var L7 = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2").filterDate(start, end).filterBounds(roi);

// Make a cloud-free mask.
function renameImage(image) {
    return image.rename(['blue', 'green', 'red', 'nir', 'swir1', 'swir2']);
}
function maskL8sr(image) {  // 去云影像
    image = ee.Image(image);
    var qa = image.select('QA_PIXEL');
    var DilatedCloud = 1 << 1; // 云层边缘
    var Cloud = 1 << 3; // 云层
    var CloudShadowBitMask = 1 << 4; // 云影
    var SnowBitMask = 1 << 5; // 积雪
    var mask = qa.bitwiseAnd(DilatedCloud).eq(0)
        .and(qa.bitwiseAnd(Cloud).eq(0))
        .and(qa.bitwiseAnd(CloudShadowBitMask).eq(0))
        .and(qa.bitwiseAnd(SnowBitMask).eq(0));
    image = image.updateMask(mask);
    // Landsat辐射定标 DN->反射率
    var opticalBands = image.select('SR_B.').multiply(0.00004).add(-0.29);
    image = image.addBands(opticalBands, null, true); // 保留属性！
    return image;
}
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
    // S2辐射定标 DN->反射率
    var opticalBands = image.select('B.', 'B..').multiply(0.0001);
    image = image.addBands(opticalBands, null, true);
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
            geometry: roi,
            bestEffort: true
        });
    return image.set("ref_mean", mean.get('mean'));
}

/*
var Landsat9 = L9.filter(ee.Filter.lt('CLOUD_COVER', 20))
                .map(maskL8sr)
                .select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5'])
                .map(renameImage)
                .map(addRefMean)
                .filter(ee.Filter.lt("ref_mean", 0.2))
                .filter(ee.Filter.gt("ref_mean", 0))
;
*/
var Landsat8 = L8.filter(ee.Filter.lt('CLOUD_COVER', 20))
    .map(maskL8sr)
    .select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'])
    .map(renameImage)
    .map(addRefMean)
    .filter(ee.Filter.lt("ref_mean", 0.2))
    .filter(ee.Filter.gt("ref_mean", 0))
    ;
/*
var Landsat7 = L7.filter(ee.Filter.lt('CLOUD_COVER', 20))
                .map(maskL8sr)
                .select(['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4'])
                .map(renameImage)
                .map(addRefMean)
                .filter(ee.Filter.lt("ref_mean", 0.2))
                .filter(ee.Filter.gt("ref_mean", 0))
;
*/
//print('L9',Landsat9.size());
//print('L8',Landsat8.size());
//print('L7',Landsat7.size());


// # Sentinel
var S2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterDate(start, end).filterBounds(roi);

// Make a cloud-free mask
var Sentinel2 = S2.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    .map(maskS2sr)
    .select(['B2', 'B3', 'B4', 'B8A', 'B11', 'B12']) //CAUTION!  select one between 'B8' and 'B8A'
    .map(renameImage)
    .map(addRefMean)
    //.filter(ee.Filter.lt("ref_mean", 0.18))
    ;


// *********
// 时间序列影像合成为Image
var yearList = ee.List.sequence(startYear, endYear, 1);
var dateList = ee.List([[[1, 1], [6, 30]], [[7, 1], [12, 31]]]);
// L8
var L8_imageList = yearList.map(function (year) {
    year = ee.Number(year);
    return dateList.map(function (days) {
        days = ee.List(days);
        var date_1 = ee.List(days.get(0));
        var date_2 = ee.List(days.get(1));
        var date_begin = ee.Date.fromYMD(year, date_1.get(0), date_1.get(1));
        var date_end = ee.Date.fromYMD(year, date_2.get(0), date_2.get(1)).advance(1, 'day');
        var images = Landsat8
            .filterDate(date_begin, date_end)
            .median()
            .clip(roi)
            .clamp(0, 1);
        return images;
    });
}).flatten();
//print("L8_imageList:", L8_imageList);

// S2
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
            .clip(roi)
            .clamp(0, 1);
        return images;
    });
}).flatten();


// S2叠到L8上
function normalize(image) {
    image = ee.Image(image);
    var RGBBands = image.select(['red', 'green', 'blue']).multiply(4);
    var NIRBands = image.select(['nir']).multiply(1.5);
    var SWIR1Bands = image.select('swir1').multiply(2);
    var SWIR2Bands = image.select('swir2').multiply(3);
    image = image.addBands(RGBBands, null, true); // 保留属性！
    image = image.addBands(NIRBands, null, true);
    image = image.addBands(SWIR1Bands, null, true);
    image = image.addBands(SWIR2Bands, null, true);
    return image;
}

var S2L8_imageList = S2_imageList.zip(L8_imageList);
var S2_and_L8 = S2L8_imageList.map(function (imageList) {
    imageList = ee.List(imageList);
    var S2_image = ee.Image(imageList.get(0));
    var L8_image = ee.Image(imageList.get(1));
    var S2L8_image = ee.Algorithms.If(
        S2_image.bandNames().length().eq(0),
        L8_image,
        ee.Algorithms.If(
            L8_image.bandNames().length().eq(0),
            S2_image,
            L8_image.blend(S2_image)
        )
    );
    var normalized_S2L8_image = normalize(S2L8_image).clamp(0, 1);
    return normalized_S2L8_image;
});

print("mix_imageList:", S2_and_L8);

for (var i = 0; i < count; i++) {
    var eeImage = ee.Image(S2_and_L8.get(i));
    var f_name = name_image.get(i).getInfo();
    // 可视化
    var visParams = {
        bands: ['red', 'green', 'blue'], // 替换为你的分类结果波段名称
        min: 0,
        max: 1,
    };
    Map.addLayer(eeImage.updateMask(eeImage.neq(0)), visParams, 'Image_' + f_name, false);

    // 导出
    Export.image.toAsset({
        image: eeImage,
        assetId: assetId + '/' + f_name,
        description: f_name,
        region: roi,
        scale: 30, //重采样使空间分辨率为30m
        crs: "EPSG:4326", //使用WGS84坐标系
        maxPixels: 1e13,
    });
}


