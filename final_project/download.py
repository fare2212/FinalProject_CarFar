#Team Members:        FARES AL HASAN       &     CARELI CABALLERO
#Date:  28/1/2016
# Project name: Crop type mapping using temporal dynamics
# Supervisor: Loic Dutrieux
#import libraries
import os
from datetime import datetime
import requests
import pytz
from fun import download_image
import geojson

#set directory
os.chdir("/home/user/git/GeoScripting/data")

#URL and API key from Planet Labs
url = "https://api.planet.com/v0/scenes/rapideye/"
key = "b932418b7f3b4b6ea86ea5408192865b"

#longitude, latitude of the selected area
sf_nw = (-122.11, 39.56)
sf_se = (-121.93, 39.46)
sf_ne = (sf_se[0], sf_nw[1])
sf_sw = (sf_nw[0], sf_se[1])

poly = geojson.Polygon([[sf_nw, sf_ne, sf_se, sf_sw, sf_nw]])
intersects = geojson.dumps(poly)

#variables for time filter
start = datetime(year=2015, month=1, day=1, tzinfo=pytz.utc).isoformat()
end = datetime(year=2016, month=1, day=25, tzinfo=pytz.utc).isoformat()

   
# Selecting scenes according to cloud cover, time and area 
params = {
    "intersects": intersects,
    "cloud_cover.estimated.lte": 0,
    "acquired.gte": start,
    "acquired.lte": end,
    "area.gte": 625.0
}

#Download rapideye images
data = requests.get(url, params=params, auth=(key, ''))
scenes_data = data.json()["features"]
for scene in scenes_data:
    thumb_link = scene["properties"]["data"]["products"]["analytic"]["full"]
    download_image(thumb_link, key)

    

   
    
    