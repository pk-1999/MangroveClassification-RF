var count = 54;

var longitude_list = ee.List.sequence(0, 360, 20);
var latitude_list = ee.List.sequence(-30, 30, 20);

var roi_list = longitude_list.map(function (longitude_start) {
    var longitude_start = ee.Number(longitude_start);
    var roi_column = latitude_list.map(function (latitude_start) {
        var latitude_start = ee.Number(latitude_start);
        return ee.Geometry.Rectangle([longitude_start, latitude_start, longitude_start.add(20), latitude_start.add(20)]);
    });
    return roi_column;
}).flatten();
//var roi = ee.Geometry.Rectangle([105,10,125,30]);

for (var i = 0; i < count; i++) {
    var roi = ee.Geometry(roi_list.get(i));
    print(roi);
    Map.addLayer(roi, { color: 'yellow' }, "area" + i);
}