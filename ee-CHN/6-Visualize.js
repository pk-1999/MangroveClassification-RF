var S2_and_L8 = ee.ImageCollection("projects/ee-pkyu1999/assets/S2_and_L8-China_v3");
var S2_and_L8_list = S2_and_L8.toList(10);

var Classified_CH = ee.ImageCollection("projects/ee-pkyu1999/assets/Classified-China-v3");
var Classified_CH_list = Classified_CH.toList(10);

var indexes = ['19-1', '19-2', '20-1', '20-2', '21-1', '21-2', '22-1', '22-2', '23-1', '23-2'];
for (var i = 0; i < 10; i++) {
    var index = indexes[i];
    var S2_and_L8_image = ee.Image(S2_and_L8_list.get(i));
    var Classified_CH_image = ee.Image(Classified_CH_list.get(i));
    var Classified_CH_display = Classified_CH_image.updateMask(Classified_CH_image.eq(1));
    Map.addLayer(S2_and_L8_image, { bands: ['nir', 'swir1', 'red'], min: 0, max: 1 }, 'S2_andL8', false);
    Map.addLayer(Classified_CH_display, { palette: ['white', 'yellow'], min: 0, max: 1 }, 'classified-' + index, false);
}

