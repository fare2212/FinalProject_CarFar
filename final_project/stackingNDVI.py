#Create a 3-D of ndvi layers
#set directory
os.chdir('/home/user/git/GeoScripting/data/')
#import libraries
import os
import rasterio
from pprint import pprint
import numpy as np
from os import listdir
import glob



#check the directory and info of the rasters
ndvi_folder_path = '/home/user/git/GeoScripting/data'
ndvi_path = glob.glob(ndvi_folder_path+'/*ndvi.tif')
print ndvi_path

from rasterstats import zonal_stats
 

#read rasters
with rasterio.open(ndvi_path[0]) as src:
    np_array = src.read(1)
    pprint(src.meta)

# Create a 3-D  empty array (rows, columns, bands)
xy =np_array.shape
np_data = np.zeros((xy[0], xy[1], len(ndvi_path)), dtype=float32)


ROWS = xy[0]
COLS = xy[1]
BANDS = len(ndvi_path)
#define characteristics of the array object
for id, file in enumerate(ndvi_path):
    with rasterio.open(file) as src:
        np_data[:,:,id] = src.read(1)
#define chaforacteristics of the array object
kwargs = src.meta
pprint(src.meta)
  # Update kwargs (change in data type)
kwargs.update(
    dtype=rasterio.float32,
    count = len(ndvi_path))  
    
with rasterio.open('NDVI_stack.tif', 'w', **kwargs) as dst:
        for i in range(np_data.shape[2]):
            dst.write_band(i+1, np_data[:,:,i].astype(rasterio.float32))

np_data=None 
!gdalinfo /home/user/git/GeoScripting/data/NDVI_stack.tif
 # Take a spatial subset of the ndvi layer produced
