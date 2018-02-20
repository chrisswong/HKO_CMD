class ForcastDay:
	def __init__(self,date,wind,weather_desc,temp_low,temp_high,rh_low,rh_high):
		self.date = date
		self.wind = wind
		self.weather_desc = weather_desc
		self.temp_low = temp_low
		self.temp_high = temp_high
		self.rh_high = rh_high
		self.rh_low = rh_low
	def __str__(self):
		return "Date: %s" % (self.date)
	def short_desc(self):
		return "Date: %s" % (self.date)