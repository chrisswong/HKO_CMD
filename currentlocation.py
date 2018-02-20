class CurrentLocationWeather:
	def __init__(self, name, degree):
		self.name = name
		self.degree = degree
	def __str__(self):
		return "%s : %g ºC" % self.name, self.degree