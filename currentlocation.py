class LocationWeather:
	def __init__(self, name, degree):
		self.name = name
		self.degree = degree
	def __str__(self):
		return "%s : %g °C" % (self.name, self.degree)