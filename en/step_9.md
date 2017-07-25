## Getting station and weather data

- Create a new Python file by clicking **File** > **New File**.
- Then use the same imports that you used in [worksheet 1](worksheet.md).

    ``` python
    from requests import get
    import webbrowser
    import folium
    import os
    ```

- This time, you'll fetch the data with a different URL. `getalllastmeasurement` will fetch data regarding all the weather stations, along with each station's last uploaded sensor reading.


    ``` python
    url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getalllastmeasurement'

    station_data = get(url).json()
    ```

- When you type `station_data['items'][0]` into your Python shell after running your script, you'll see that there is a lot of information provided by the RESTful API. If you follow this resource exactly, you will extract the temperature data as well as station longitudes and latitudes. If you want to use data from a different sensor though, that's fine.

    ``` json
    {'reading_timestamp': '2016-11-20T21:55:02Z', 'weather_stn_lat':
    40.658055, 'wind_gust_speed': 0, 'weather_stn_id': 1704961, 'rainfall':
    0, 'air_pressure': 962.21, 'humidity': 38.9, 'weather_stn_long':
    22.921949, 'ground_temp': 19.44, 'wind_speed': 0, 'wind_direction':
    270, 'weather_stn_name': 'Ampelokhpoi Weather Station', 'air_quality':
    50.52, 'ambient_temp': 25.15}
    ```

- It is possible that some weather stations do not use all their sensors. If some stations do not measure temperature, they will upload rows of records to the database that don't contain temperature readings. This would lead to failure of the list comprehensions you used in [worksheet 1](worksheet.md). Therefore you need to use a slightly longer - but more resilient - method to fetch the records.

    ``` python
    temps = []
    tmax = 0.0
    tmin = 100.0
    lons = [data['weather_stn_long'] for data in station_data['items']]
    lats = [data['weather_stn_lat'] for data in station_data['items']]
    wsnames = [station['weather_stn_name'] for station in station_data['items']]
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

