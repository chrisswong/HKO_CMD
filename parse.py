import xmltodict
from bs4 import BeautifulSoup
import currentlocation

curr_weather_url = "http://rss.weather.gov.hk/rss/CurrentWeather.xml"
forecast_weather_url = "http://rss.weather.gov.hk/rss/SeveralDaysWeatherForecast.xml"

with open('./CurrentWeather.xml') as fd:
    doc = xmltodict.parse(fd.read())
    curr_weather = doc['rss']['channel']['item']['description']
    # curr_weather_doc = xmltodict.parse("<?xml version=\"1.0]\"?>\n" + curr_weather)
    soup = BeautifulSoup(curr_weather, 'html.parser')
    location_weather = soup.find_all('tr')
    locations = []
    for l in location_weather:
    	c = currentlocation("")
    	locations.append()
