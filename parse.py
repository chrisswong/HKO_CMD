import xmltodict
from bs4 import BeautifulSoup
from currentlocation import LocationWeather

curr_weather_url = "http://rss.weather.gov.hk/rss/CurrentWeather.xml"
forecast_weather_url = "http://rss.weather.gov.hk/rss/SeveralDaysWeatherForecast.xml"

is_json = True
is_all_location = True

def remove_all_alphabet(s):
	return "".join([i for i in s if i.isdigit()]).strip()

with open('./CurrentWeather.xml') as fd:
	doc = xmltodict.parse(fd.read())
	curr_weather_description = doc['rss']['channel']['item']['description']
	soup = BeautifulSoup(curr_weather_description, 'html.parser')
	if not is_all_location:
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
						curr_weather[curr_weather_index_to_key[x]] = float(b)
					else:
						b = curr_weather_list[x].split(":")[1].strip()
						curr_weather[curr_weather_index_to_key[x]] = b 
		if is_json:
			import json
			print(json.dumps(curr_weather, indent=4, sort_keys=True))
		else:
			import pprint
			pprint.pprint(curr_weather)
	else:
		locations = []
		all_tr = soup.find_all('tr')
		for tr in all_tr:
			all_td = tr.find_all('td')
			l =  LocationWeather(all_td[0].get_text(), float(remove_all_alphabet(all_td[1].get_text())))
			locations.append(l)
			# for td in all_td:
			# l = 
		for l in locations:
			print(l)



