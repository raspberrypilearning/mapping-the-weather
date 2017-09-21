import requests
import json
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallstations'

weather = requests.get(url).json()

cc_lat = 55
cc_lon = 0

my_map = Basemap(projection='merc', lat_0 = cc_lat, lon_0 = cc_lon,
                 resolution = 'h' , area_thresh = 1,
                 llcrnrlon=cc_lon-15, llcrnrlat=cc_lat-7,
                 urcrnrlon=cc_lon+5, urcrnrlat=cc_lat+5)

my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color='green')

lons = [record['weather_stn_long'] for record in weather['items']]
lats = [record['weather_stn_lat'] for record in weather['items']]

x,y = my_map(lons, lats)
my_map.plot(x, y, 'bo', markersize=12)

plt.show()
