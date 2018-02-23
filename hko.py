def show_location_weather(l):
	d = dict({"abc" : 1})
	print("show_location_weather = %s" % l)
	return d

def save_string_to_file(string="", filename="filename", binary_mode=False):
	if not binary_mode:
		mode = 'w'
	else:
		mode = 'wb'
	file = open(filename, mode)
	file.write(string)
	file.close()

import argparse
import pprint
from WeatherParser import CurrentWeatherParser
from WeatherParser import ForecastWeatherParser

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()
group.add_argument("-c", "--complete", help="show current HKO weather and all location weather.", action="store_true")
group.add_argument("-n", "--now", help="show current HKO weather.", action="store_true")
group.add_argument("-a", "--all", help="show all location current temp.", action="store_true")
group.add_argument("-f", "--forecast", help="show upcoming [1-9] days forecast. ", type=int)
group.add_argument("-l", "--location", help="show specify location current temp.")


parser.add_argument("-v", "--verbose", help="show debug message")
parser.add_argument("-o", "--output", choices=['xml','json'], help="output as selected file format")

args = parser.parse_args()

if any(vars(args).values()):
	d = dict()
	if args.complete:
		c = CurrentWeatherParser()
		d1 = c.current_weather()
		d2 = c.location_weather()
		for k in d1.keys():
			d[k] = d1[k]
		for k in d2.keys():
			d[k] = d2[k]
	elif args.now: 
		c = CurrentWeatherParser()
		d = c.current_weather()
	elif args.all:
		c = CurrentWeatherParser()
		d = c.location_weather()
	elif args.forecast > 0:
		f = ForecastWeatherParser()
		d = f.forecast(args.forecast)
	elif len(args.location) > 0:
		c = CurrentWeatherParser()
		d = c.location_weather(args.location)

	if args.output and len(args.output) > 0:
		filename = "output."+ args.output
		if args.output == 'xml':
			from dicttoxml import dicttoxml
			from xml.dom.minidom import parseString
			xml = dicttoxml(d, custom_root='hko', attr_type=False)
			dom = parseString(xml)
			save_string_to_file(dom.toprettyxml(), filename)
		elif args.output == 'json':
			import json
			json_string = json.dumps(d, indent=4, sort_keys=True)
			save_string_to_file(json_string, filename)
	else:
		pprint.pprint(d)
else:
	parser.print_help()