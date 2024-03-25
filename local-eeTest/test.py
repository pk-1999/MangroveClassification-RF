import ee
ee.Authenticate()
ee.Initialize(project='ee-pkyu1999')
print(ee.Image("NASA/NASADEM_HGT/001").get("title").getInfo())
image_test = ee.Image('srtm90_v4')
path = image_test.getDownloadUrl({
    'scale':30,
    'crs':'EPSG:4326',
    'region':'[[-120, 35], [-119, 35], [-119, 34], [-120,34]]'
})
print(path)

