# HKO_CMD
A python command line program to retrieve Hong Kong Observary's weather data.

-- 

# Usage

```
$ python3 hko.py -h 
usage: hko.py [-h] [-c | -n | -a | -f | -l LOCATION] [-v VERBOSE]
              [-o {xml,json}]

optional arguments:
  -h, --help            show this help message and exit
  -c, --complete        show current HKO weather and all location weather.
  -n, --now             show current HKO weather.
  -a, --all             show all location current temp.
  -f, --forecast        show upcoming forecast.
  -l LOCATION, --location LOCATION
                        show specify location current temp.
  -v VERBOSE, --verbose VERBOSE
                        show debug message
  -o {xml,json}, --output {xml,json}
                        output as selected file format
```

--
## Work In Process

1. Parsing Forecast data [Done]
2. Getting location-specific current weather
3. Add debug message for ```-v```
4. Add ```-s``` for serving json and xml with Flask
5. Add current weather alerts 
6. Better json data type instead of using strings