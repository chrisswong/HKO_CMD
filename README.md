# HKO_CMD
A python command line program to retrieve Hong Kong Observary's weather data.

# Usage

```
$ python3 hko.py -h 
usage: hko.py [-h] [-c | -n | -a | -s | -f FORECAST | -l LOCATION]
              [-v VERBOSE] [-o {xml,json}]

optional arguments:
  -h, --help            show this help message and exit
  -c, --complete        show current HKO weather and all location weather.
  -n, --now             show current HKO weather.
  -a, --all             show all location current temp.
  -s, --server          start a flask server for serving json and xml (Go to
                        http://127.0.0.1:5000 for description)
  -f FORECAST, --forecast FORECAST
                        show upcoming [1-9] days forecast.
  -l LOCATION, --location LOCATION
                        show specify location current temp.
  -v VERBOSE, --verbose VERBOSE
                        show debug message
  -o {xml,json}, --output {xml,json}
                        output as selected file format
```

## Work In Process

1. Parsing Forecast data [Done]
2. Getting location-specific current weather [Done]
3. Add debug message for ```-v```
4. Add ```-s``` for serving json and xml with Flask [Done]
5. Add current weather alerts 
6. Better json data type instead of using strings
7. Cache mechanism - only download/retrieve new weather data after period of time