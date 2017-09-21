## Creating a map

- The first thing to do is to set up your map.

    ``` python
    map_ws = folium.Map(location=[0,0],zoom_start=2)
    ```

- This creates a map centred at latitude 0, longitude 0.

- Save your map as a local html file and open it using a web browser. Python's `os` library is used to discover the Current Working Directory (CWD) so that the browser knows from where to load the saved map file.

    ``` python
    CWD = os.getcwd()
    map_ws.save('wsmap1.html')
    webbrowser.open_new('file://'+CWD+'/'+'wsmap1.html')
    ```

- Save and run your file. A new browser window should open up, displaying a map of the globe.

![basic map](images/basic_map.png)


