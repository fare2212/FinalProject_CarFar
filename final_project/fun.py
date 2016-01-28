#import libraries
import requests
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32
import numpy as np
import matplotlib.pyplot as plt
import glob

#FUNCTION FOR DOWNLOADING IMAGES
def download_image(url, key):
    r = requests.get(url, stream=True, auth=(key, ''))
    if 'content-disposition' in r.headers:
        local_filename = r.headers['content-disposition'] \
            .split("filename=")[-1].strip("'\"")
    else:
        local_filename = '.'.join(url.split('/')[-2:])

    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()

    return local_filename
    


#FUNCTION FOR CALCULATING NDVI
def image_ndvi(inputD,outputD):
    dataSource = gdal.Open(inputD, GA_ReadOnly)
    geotransform = dataSource.GetGeoTransform()
    if not geotransform is None:
        print 'Origin = (',geotransform[0], ',',geotransform[3],')'
        print 'Pixel Size = (',geotransform[1], ',',geotransform[5],')'
    #read data into Array
    band3Arr = dataSource.GetRasterBand(3).ReadAsArray(0,0,dataSource.RasterXSize, dataSource.RasterYSize)
    band5Arr = dataSource.GetRasterBand(5).ReadAsArray(0,0,dataSource.RasterXSize, dataSource.RasterYSize)
    print type(band3Arr)
    print type(band5Arr)
                                                   
    # set the data type
    band3Arr=band3Arr.astype(np.float32)
    band5Arr=band5Arr.astype(np.float32)

    # Derive the NDVI
    mask = np.greater(band3Arr+band5Arr,0)

    # set np.errstate to avoid warning of invalid values (i.e. NaN values) in the divide 
    with np.errstate(invalid='ignore'):
        ndvi = np.choose(mask,(-99,(band5Arr-band3Arr)/(band5Arr+band3Arr)* 10000)) 
        
    # Write the result to disk
    driver = gdal.GetDriverByName('GTiff')
    outDataSet=driver.Create(outputD, dataSource.RasterXSize, dataSource.RasterYSize, 1, GDT_Float32)
    outBand = outDataSet.GetRasterBand(1)
    outBand.WriteArray(ndvi,0,0)
    outBand.SetNoDataValue(-99)

    # set the projection and extent information of the dataset
    outDataSet.SetProjection(dataSource.GetProjection())
    outDataSet.SetGeoTransform(dataSource.GetGeoTransform())

    #save the file
    outBand.FlushCache()
    outDataSet.FlushCache()
    
    # Take a spatial subset of the ndvi layer produced
    ndvi_sub = ndvi[1000:2000, 1000:2000]

    # Plot
    plt.imshow(ndvi_sub)

    plt.show()
    
   
     

