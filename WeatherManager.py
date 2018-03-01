from WeatherParser import CurrentWeatherParser
from WeatherParser import RegionWeatherParser
from WeatherParser import ForecastWeatherParser

class WeatherManager():

	def complete(self):
		c = CurrentWeatherParser()
		d = c.current_weather()
		r = RegionWeatherParser()
		d2 = r.retrieve()
		d["location_weather"] = d2
		return d

	def now(self):
		c = CurrentWeatherParser()
		d = c.current_weather()
		return d

	def all_location(self):
		r = RegionWeatherParser()
		d = r.retrieve()
		return d

	def location(self,location=""):
		r = RegionWeatherParser()
		if len(location) > 0:
			d = r.retrieve(location)
		return d

	def forecast(self,days = 9):
		f = ForecastWeatherParser()
		d = f.forecast(days)
		return d
		

