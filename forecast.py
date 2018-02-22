class Forecast:
	def __init__(self,date,wind,weather_desc,temp,rh):
		self.date = date
		self.wind = wind
		self.weather_desc = weather_desc
		self.temp = temp
		self.rh = rh
		# self.temp_low = temp_low
		# self.temp_high = temp_high
		# self.rh_high = rh_high
		# self.rh_low = rh_low
	def __str__(self):
		return "%s %s %s %s %s" % (self.date, self.wind, self.weather_desc, self.temp, self.rh)
	def short_desc(self):
		return "Date: %s" % (self.date)