#load vectors into GeoDataFrames and rasters into ndarrays and inspect the results. 
#Then we'll run zonal statistics on the two datasets, bring it back into a GeoDataFrames and write the results to a GeoJSON file.
import os
os.chdir ("/home/user/git/GeoScripting/data")
import geojson
import geopandas as gpd
geodf = gpd.GeoDataFrame.from_file('/home/user/git/GeoScripting/data/Field_map.shp')
geodf.plot()
geodf
import rasterio
with rasterio.open("/home/user/git/GeoScripting/data/NDVI_stack.tif") as src:
    transform = src.meta['transform']
    array = src.read_band(1)
    
print (transform)
array
from rasterstats import zonal_stats
stats = zonal_stats(geodf, array, transform=transform, stats="*")
stats


from pprint import pprint
pprint (stats)
zonal_stats