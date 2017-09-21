from requests import get
import webbrowser
import folium
import os
import html

CWD = os.getcwd()


def colourgrad(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    g = int(max(0, 255*(ratio - 1)))
    r = 255 - b - g
    hexcolour = '#%02x%02x%02x' % (r,g,b)
    return hexcolour


url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getalllastmeasurement'
stations = get(url).json()
temps = []
tmax = 0.0
tmin = 100.0
print('Downloading data')
lons = [station['weather_stn_long'] for station in stations['items']]
lats = [station['weather_stn_lat'] for station in stations['items']]
WSnames = [html.escape(station['weather_stn_name'] ) for station in stations['items']]
for data in stations['items']:
    # if data['weather_stn_id'] != 1002485:
    if 'ambient_temp' in data:   # check value isn't missing
        t = data['ambient_temp']
        if t > 50 or t < -30:   # ignore silly values
            t = 20
        if t > tmax:
            tmax = t
        if t < tmin:
            # print(t, data['weather_stn_id'])
            tmin = t
        temps.append(str(t))
map_osm = folium.Map(location=[0, 0], zoom_start=2)
print('Max and Min temperatures: ' + str(tmax) + ' and ' +  str(tmin))
for n in range(len(lons)-1):
    hcol = colourgrad(tmin, tmax, float(temps[n]))
    #hcol = '#%02x%02x%02x' % hcolrgb
    # print(hcol)
    # folium.Marker([lats[n], lons[n]], popup=temps[n], icon=folium.Icon(color = hcol,icon='cloud')).add_to(map_osm)
    folium.CircleMarker([lats[n], lons[n]],
                        radius = 5,
                        popup = WSnames[n]+':'+temps[n],
                        fill_color = hcol).add_to(map_osm)
    print('Process WS number:' + str(n) + ':' + WSnames[n])

map_osm.save('osm.html')
print('map saved')
webbrowser.open_new('file://'+CWD+'/'+'osm.html')
