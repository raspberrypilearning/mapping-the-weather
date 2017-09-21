# Mapping the Weather

## Getting station and weather data

1. Create a new Python file by clicking **File** > **New File**.
1. Then use the same imports that you used in [worksheet 1](worksheet.md).

    ``` python
    from requests import get
    import webbrowser
    import folium
    import os
    import html
    ```

1. This time, you'll fetch the data with a different URL. `getalllastmeasurement` will fetch data regarding all the weather stations, along with each station's last uploaded sensor reading.


    ``` python
    url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getalllastmeasurement'

    station_data = get(url).json()
    ```

1. When you type `station_data['items'][0]` into your Python shell after running your script, you'll see that there is a lot of information provided by the RESTful API. If you follow this resource exactly, you will extract the temperature data as well as station longitudes and latitudes. If you want to use data from a different sensor though, that's fine.

    ``` json
    {'reading_timestamp': '2016-11-20T21:55:02Z', 'weather_stn_lat':
    40.658055, 'wind_gust_speed': 0, 'weather_stn_id': 1704961, 'rainfall':
    0, 'air_pressure': 962.21, 'humidity': 38.9, 'weather_stn_long':
    22.921949, 'ground_temp': 19.44, 'wind_speed': 0, 'wind_direction':
    270, 'weather_stn_name': 'Ampelokhpoi Weather Station', 'air_quality':
    50.52, 'ambient_temp': 25.15}
    ```

1. It is possible that some weather stations do not use all their sensors. If some stations do not measure temperature, they will upload rows of records to the database that don't contain temperature readings. This would lead to failure of the list comprehensions you used in [worksheet 1](worksheet.md). Therefore you need to use a slightly longer - but more resilient - method to fetch the records.

    ``` python
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
    ```
The online database of weather measurements also contains test data from when schools set up their stations. Some of these readings are not accurate - for example, one temperature sensor was reporting values of -1000 degrees. That's colder than absolute zero!

To ensure that these values are ignored, the code above will also check for values less than -30 and greater than 50 degrees and set any readings that fall outside this range to an abitrary 20 degrees. The final step is to use the variables `tmax` and `tmin` to keep track of the maximum and minimum recorded temperatures. These values will be used to create a colour scale so that the markers plotted on the map give a visual indication of the temperature they represent.

## Defining a colour scale

Add the `colourgrad` function immediately below the `import` declarations at the top of the file. This function takes a value and assigns a RGB colour to it depending on the maximum and minimum temperature values. The RGB colour is converted into hexadecimal notation suitable for use with `folium` markers.

```python
def colourgrad(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    g = int(max(0, 255*(ratio - 1)))
    r = 255 - b - g
    hexcolour = '#%02x%02x%02x' % (r,g,b)
    return hexcolour
```
Our map is going to display temperature values, so we're setting the colour range to blue for the coldest measurements and green for the hottest, with most of the mid-range temperatures plotted in red. If you're visualising data from a different sensor, you can hack the `colourgrad` function to use colours in a different way.

## Setting up the map

You can set your map up in more or less the same way as in [worksheet 1](worksheet.md).

``` python
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
```
The main difference is that a custom circular marker is used to allow colours to represent different temperatures.

1. Run your code and you should see your map.

![uk](images/temp_map.png)

## What Next

Why not try and plot some other sensor data, like rainfall?

There is a lot more functionality in `folium` that you can explore. You could, for example, try and use a choropleth map to display weather station data based on regions.
