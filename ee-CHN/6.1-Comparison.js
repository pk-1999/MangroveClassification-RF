var GMD_GM2020 = ee.FeatureCollection("projects/ee-pkyu1999/assets/mangrove/GlobalMangrove2020"),
    GMD_MC2015 = ee.FeatureCollection("projects/ee-pkyu1999/assets/mangrove/MangroveChina2015_DC_Correction"),
    GMD_MMC2019 = ee.FeatureCollection("projects/ee-pkyu1999/assets/mangrove/mangrove_of_China_for_2019");

var S2_and_L8 = ee.Image("projects/ee-pkyu1999/assets/S2_and_L8-China_v3/23-2");
var Classified_CH = ee.Image("projects/ee-pkyu1999/assets/Classified-China-v3/23-2");

var Classified_CH_display = Classified_CH.updateMask(Classified_CH.eq(1));
Map.addLayer(S2_and_L8, { bands: ['nir', 'swir1', 'red'], min: 0, max: 1 }, 'S2_andL8');
Map.addLayer(Classified_CH_display, { palette: ['white', 'yellow'], min: 0, max: 1 }, 'classified', false);


var roi = ee.Geometry.Rectangle([109.0, 19.8, 111.0, 21.8]); // ZhanJiang
var GMD = GMD_MMC2019;
var RMD = GMD.filterBounds(roi);
// 在 RMD 中设置 'value' 属性为 1
RMD = RMD.map(function (feature) {
    return feature.set('value', 1);
});
// 将 FeatureCollection 转换为 Image
var img_RMD = RMD.reduceToImage(['value'], ee.Reducer.first()).eq(1);
Map.addLayer(img_RMD, { min: 0, max: 1, palette: ['white', 'yellow'] }, 'Reference');
