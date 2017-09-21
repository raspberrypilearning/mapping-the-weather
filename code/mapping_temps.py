from requests import get
import webbrowser
import folium
import os
import html

def colourgrad(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    g = int(max(0, 255*(ratio - 1)))
    r = 255 - b - g
    hexcolour = '#%02x%02x%02x' % (r,g,b)
    return hexcolour

url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getalllastmeasurement'

station_data = get(url).json()

temps = []
tmax = 0.0
tmin = 100.0
lons = [data['weather_stn_long'] for data in station_data['items']]
lats = [data['weather_stn_lat'] for data in station_data['items']]
wsnames = [html.escape(station['weather_stn_name'] ) for station in station_data['items']]
for data in station_data['items']:
    if 'ambient_temp' in data:
        t = data['ambient_temp']
        if t > 50 or t < -30:
            t = 20
        if t > tmax:
            tmax = t
        if t < tmin:
            tmin = t
        temps.append(str(t))

map_ws = folium.Map(location=[0, 0], zoom_start=2)
for n in range(len(lons)-1):
    hcol = colourgrad(tmin, tmax, float(temps[n]))
    folium.CircleMarker([lats[n], lons[n]],
                        radius = 5,
                        popup = wsnames[n]+':'+temps[n],
                        fill_color = hcol).add_to(map_ws)

CWD = os.getcwd()
map_ws.save('osm.html')
webbrowser.open_new('file://'+CWD+'/'+'osm.html')
