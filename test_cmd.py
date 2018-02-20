
def showCurrentHKOWeather():
	d = dict({"abc" : 1})
	print("showCurrentHKOWeather")
	return d

def showCurrentAllLocationWeather():
	d = dict({"abc" : 1})
	# d = dict()
	print("showCurrentAllLocationWeather")
	return d

def show_forecast():
	d = dict({"abc" : 1})
	# d = dict()
	print("show_forecast")
	return d

def show_location_weather(l):
	d = dict({"abc" : 1})
	# d = dict()
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
parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()
group.add_argument("-c", "--complete", help="show current HKO weather and all location weather.", action="store_true")
group.add_argument("-n", "--now", help="show current HKO weather.", action="store_true")
group.add_argument("-a", "--all", help="show all location current temp.", action="store_true")
group.add_argument("-f", "--forecast", help="show upcoming forecast.", action="store_true")
group.add_argument("-l", "--location", help="show specify location current temp.")


parser.add_argument("-v", "--verbose", help="show debug message")
parser.add_argument("-o", "--output", choices=['xml','json'], help="output as selected file format")

args = parser.parse_args()
d = dict()
if args.complete:
	showCurrentHKOWeather()
	showCurrentAllLocationWeather()
elif args.now: 
	d = showCurrentHKOWeather()
elif args.all:
	d = showCurrentAllLocationWeather()
elif args.forecast:
	d = show_forecast()
elif len(args.location) > 0:
	d = show_location_weather(args.location)

if args.output and len(args.output) > 0:
	filename = "output."+ args.output
	if args.output == 'xml':
		from dicttoxml import dicttoxml
		from xml.dom.minidom import parseString
		xml = dicttoxml(d, custom_root='weather', attr_type=False)
		dom = parseString(xml)
		save_string_to_file(dom.toprettyxml(), filename)
	elif args.output == 'json':
		import json
		json_string = json.dumps(d, indent=4, sort_keys=True)
		save_string_to_file(json_string, filename)








# nothing -> current HKO weather
# -a --all -> shows all location 
# -l --location [location name] -> show that location name
# -f --forecast -> show all forecast
# -v --verbose -> show debug message
# anything with -j  -> standard output as json format
# anything with -o {json|xml} [filename] -> output as filename with json or xml