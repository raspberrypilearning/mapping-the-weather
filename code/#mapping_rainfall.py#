from requests import get
import json
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getalllastmeasurement'

station_data = get(url).json()

print('got data')
lons = [data['weather_stn_long'] for data in station_data['items']]
lats = [data['weather_stn_lat'] for data in station_data['items']]
temps = [data['ambient_temp'] for data in station_data['items']]
print('processed data')
cc_lat = 55
cc_lon = 0

my_map = Basemap(projection='robin', lat_0 = cc_lat, lon_0 = cc_lon,
                 resolution = 'l')
print('map created')
my_map.drawcoastlines()
my_map.drawcountries()

my_map.drawmapboundary()
my_map.bluemarble()

print('Starting zip')
for lon, lat, temp in zip(lons, lats, temps):
    x,y = my_map(lon, lat)
    my_map.plot(x, y, 'o', markersize=10, color=(0,0,1))
    plt.text(x, y, temp, color = 'w', ha='right',va='bottom')
print('ending zip')
plt.show()
