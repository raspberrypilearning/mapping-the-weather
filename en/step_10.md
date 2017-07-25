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

