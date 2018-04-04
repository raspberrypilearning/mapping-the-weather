## Fetching the weather stations

If you want to know more about using JSON and the RESTful API of the Raspberry Pi weather station database, have a look over the resources [Fetching the weather](https://projects.raspberrypi.org/en/projects/fetching-the-weather/) and [Graphing the weather](https://projects.raspberrypi.org/en/projects/graphing-the-weather/).

- This guide is written for a Raspberry Pi, but the code should work on any computer that has Python 3 installed. You can find out more about installing Python on differnet types of computers [here](https://wiki.python.org/moin/BeginnersGuide).

- Open a new Python shell by clicking on **Menu** > **Programming** > **Python 3 (IDLE)**. Then click **File** > **New File** to start a new script.


    ``` python
    from requests import get
    import json
    import folium
    import os
    import webbrowser
    import html
    ```

- Here, `requests` is used to fetch the JSON data from the database, and `json` to process JSON data. `folium` is a tool for visualising data on maps in Python.

- Next, the URL for the RESTful API needs to be stored as a string in your program.

    ``` python
    url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallstations'
    ```

- Then, the JSON data can be fetched.

    ``` python
    stations = get(url).json()
    ```

- Save and run this file to fetch the data. You will be able to examine the data, for example by typing the following into the Python shell:

    ``` python
    stations['items'][0]
    ```

- You should see something like this printed out in the shell:


    ``` python
    {'weather_stn_name': 'Pi Towers Demo', 'weather_stn_id': 255541, 'weather_stn_long': 0.110421, 'weather_stn_lat': 52.213842}
    ```

- This is the first record in the JSON data set. As you can see, the station's longitude and latitude are within the dictionary. If you want to learn a little more about longitudes and latitudes, have a look at the [second worksheet of this resource](https://projects.raspberrypi.org/en/projects/fetching-the-weather/worksheet2). The longitude and latitude values are easy to access. For instance, to find out the longitude of the first station in the dictionary, type this into the shell:


    ``` python
    stations['items'][0]['weather_stn_long']
    ```

    If you wanted to see the value of a different station, type this:


    ``` python
    stations['items'][5]['weather_stn_long']
    ```

- Add three list comprehensions to your Python file to fetch all the longitude and latitude values along with the names of the weather stations. These commands iterate over the JSON data and extract each of the longitudes, latitudes, and names and place them in separate lists. When school's register their weather station names, they can use characters, especially punctuation like apostrophes, that may cause problems when used within HTML tags. Converting these characters to a safe format is called *escaping* and the Python html library has a handy function for just this job.

    ``` python
    lons = [station['weather_stn_long'] for station in stations['items']]
    lats = [station['weather_stn_lat'] for station in stations['items']]
    wsnames = [html.escape(station['weather_stn_name']) for station in stations['items']]
    ```

- Now run your file. You can have a look at all the weather station names by typing the following into the shell:

``` python
wsnames
```
