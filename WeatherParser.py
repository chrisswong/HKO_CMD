import os
import xmltodict
from bs4 import BeautifulSoup
from currentlocation import LocationWeather
import wget

from forecast import Forecast

class Parser:
	def remove_all_alphabet(self,s):
		return "".join([i for i in s if i.isdigit()]).strip()

	def delete_file(self,filename):
		if os.path.exists(filename):
			os.remove("./"+filename)

	def download(self): 
		wget.download(self.download_xml_url,self.xml_file, False)

	def clean_up(self):
		self.delete_file(self.xml_file)

class CurrentWeatherParser(Parser):
	def __init__(self):
		self.xml_file = "./current.xml"
		self.download_xml_url = "http://rss.weather.gov.hk/rss/CurrentWeather.xml"

	def __parse(self):
		with open(self.xml_file) as fd:
			doc = xmltodict.parse(fd.read())
			curr_weather_description = doc['rss']['channel']['item']['description']
			soup = BeautifulSoup(curr_weather_description, 'html.parser')
			return soup

	def __current_weather(self, soup):
		text_list = soup.find('p').get_text()

		text_list = text_list.split('\n')

		clean_text_list = [a.strip() for a in text_list]

		curr_weather = dict()

		curr_weather_list = clean_text_list[1:8]

		curr_weather_index_to_key = {0: "time", 2:"temp", 3:"humid", 5:"UI_index", 6:"UI_intensity"}
		for x in range(0,len(curr_weather_list)):
			if x in [0,2,3,5,6]:
				if ":" not in curr_weather_list[x]:
					curr_weather[curr_weather_index_to_key[x]] = curr_weather_list[x]
				else:
					b = curr_weather_list[x].split(":")[1].strip()
					if x in [2,3,5]:
						b = "".join([i for i in b if not i.isalpha()]).strip()
						if len(b) > 0:
							curr_weather[curr_weather_index_to_key[x]] = float(b)
						else:
							curr_weather[curr_weather_index_to_key[x]] = ""
					else:
						b = curr_weather_list[x].split(":")[1].strip()
						curr_weather[curr_weather_index_to_key[x]] = b 

		return { "CurrentWeather": curr_weather }

	def __loction_weather(self, soup):
		locations = []
		all_tr = soup.find_all('tr')
		for tr in all_tr:
			all_td = tr.find_all('td')
			l =  LocationWeather(all_td[0].get_text(), float(self.remove_all_alphabet(all_td[1].get_text())))
			locations.append(str(l))
		return {"location_weather": locations}

	def current_weather(self):
		self.download()
		soup = self.__parse()
		d = self.__current_weather(soup)
		self.clean_up()
		return d 

	def location_weather(self, location=""):
		self.download()
		soup = self.__parse()
		d = self.__loction_weather(soup)
		if len(location) > 0:
			l = [ x for x in d["location_weather"] if location in x ]
			d["location_weather"] = l
		self.clean_up()
		return d

class ForecastWeatherParser(Parser):
	def __init__(self):
		self.xml_file = "./forecast.xml"
		# self.xml_file = "./SeveralDaysWeatherForecast.xml"
		self.download_xml_url = "http://rss.weather.gov.hk/rss/SeveralDaysWeatherForecast.xml"

	def __forecast(self, soup, num_of_days_of_forecast):
		keys = ["Date/Month:", "Wind:", "Weather:" , "Temp range:", "R.H. range:"]
		l = soup.get_text().split('\n')
		forecast_list = []
		# b = []
		# for a in l:
		date = ""
		wind = ""
		weather = ""
		temp = ""
		rh = ""
		last_date = ""
		is_first_date = True
		for i in range(0, len(l)):
			s = l[i].strip()
			if i + 2 < len(l):
				if s == keys[0]:
					date = l[i+1].strip()
				elif s == keys[1]:
					wind = l[i+1].strip()
				elif s == keys[3]:
					temp = l[i+1].strip() + " " + l[i+2].strip()
				elif s == keys[4]:
					rh = l[i+1].strip() + " " + l[i+2].strip() 
				elif s == keys[2]:
					weather = l[i+1].strip() 
				if len([x for x in [date, wind, weather, temp, rh] if len(x) > 0]) == 5:
					f = Forecast(date, wind, weather, temp, rh)
					forecast_list.append(f.dict())
					date = ""
					wind = ""
					weather = ""
					temp = ""
					rh = ""

		return {"general_situation" : l[0].split(":")[1], "forecast" : forecast_list[0:num_of_days_of_forecast] }

	def __parse(self):
		with open(self.xml_file) as fd:
			doc = xmltodict.parse(fd.read())
			curr_weather_description = doc['rss']['channel']['item']['description']
			soup = BeautifulSoup(curr_weather_description, 'html.parser')
			return soup

	def forecast(self, num_of_days_of_forecast = 9):
		self.download()
		soup = self.__parse()
		if num_of_days_of_forecast > 9 or num_of_days_of_forecast < 0:
			num_of_days_of_forecast = 9

		d = self.__forecast(soup, num_of_days_of_forecast)
		self.clean_up()
		return d


