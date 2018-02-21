import os
import xmltodict
from bs4 import BeautifulSoup
from currentlocation import LocationWeather
import wget

class Parser:
	def remove_all_alphabet(self,s):
		return "".join([i for i in s if i.isdigit()]).strip()

	def delete_file(self,filename):
		if os.path.exists(filename):
			os.remove("./"+filename)

	def download(self): 
		wget.download(self.curr_weather_url,self.xml_file, False)

	def clean_up(self):
		self.delete_file(self.xml_file)

class CurrentWeatherParser(Parser):
	def __init__(self):
		self.xml_file = "./current.xml"
		self.curr_weather_url = "http://rss.weather.gov.hk/rss/CurrentWeather.xml"

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

		return curr_weather

	def __loction_weather(self, soup):
		locations = []
		all_tr = soup.find_all('tr')
		for tr in all_tr:
			all_td = tr.find_all('td')
			l =  LocationWeather(all_td[0].get_text(), float(self.remove_all_alphabet(all_td[1].get_text())))
			locations.append(str(l))
		return {"location_weather": locations}

	def current_weather(self):
		self.download();
		soup = self.__parse()
		d = self.__current_weather(soup)
		self.clean_up()
		return d 

	def location_weather(self, location=""):
		self.download();
		soup = self.__parse()
		d = self.__loction_weather(soup)
		self.clean_up()
		return d

class ForecastWeatherParser(Parser):
	def __init__(self):
		self.xml = "./forecast.xml"
		self.forecast_weather_url = "http://rss.weather.gov.hk/rss/SeveralDaysWeatherForecast.xml"

