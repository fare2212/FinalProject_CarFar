#calculat ndvi for each scene
#set directory
os.chdir("/home/user/git/GeoScripting/data")
#import libraries
import os
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32
import numpy as np
import matplotlib.pyplot as plt
import glob
from fun import image_ndvi



#Select images for aplying NDVI
SceneFolderPath = '/home/user/git/GeoScripting/data/'
ScenePath = glob.glob(SceneFolderPath+'/*analytic.tif')
print ScenePath  

#defining output directory and name for the NDVI images 
for scene in ScenePath:
    output= str(scene).replace("analytic","ndvi")
    
    image_ndvi(scene,output)