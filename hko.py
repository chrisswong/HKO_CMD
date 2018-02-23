import argparse
import pprint
from WeatherParser import CurrentWeatherParser
from WeatherParser import ForecastWeatherParser
from flask import Flask 
from flask import jsonify
from flask import Response

def save_string_to_file(string="", filename="filename", binary_mode=False):
	if not binary_mode:
		mode = 'w'
	else:
		mode = 'wb'
	file = open(filename, mode)
	file.write(string)
	file.close()


def handle_format(data, format):
	if format == 'json':
		return jsonify(data)
	elif format == 'xml':
		from dicttoxml import dicttoxml
		xml = dicttoxml(data, custom_root='hko', attr_type=False)
		r = Response(response=xml, status=200, mimetype="application/xml")
		r.headers["Content-Type"] = "text/xml; charset=uft-8"
		return r
	else:
		return "Unknown format"

app = Flask(__name__)

@app.route('/now/<format>')
def now(format):
	c = CurrentWeatherParser()
	d = c.current_weather()
	return handle_format(d, format)

@app.route('/complete/<format>')
def complete(format):
	c = CurrentWeatherParser()
	d1 = c.current_weather()
	d2 = c.location_weather()
	for k in d1.keys():
		d[k] = d1[k]
	for k in d2.keys():
		d[k] = d2[k]
	return handle_format(d, format)

@app.route('/all/<format>')
def all(format):
	c = CurrentWeatherParser()
	d = c.location_weather()
	return handle_format(d, format)

@app.route('/forecast9Days/<format>')
def forecast9Days(format):
	f = ForecastWeatherParser()
	d = f.forecast()
	return handle_format(d, format)

@app.route('/forecast/<int:num_of_days>/<format>')
def forecast(num_of_days, format):
	f = ForecastWeatherParser()
	d = f.forecast(num_of_days)
	return handle_format(d, format)

@app.route('/location/<keyword>')
def location(format):
	c = CurrentWeatherParser()
	d = c.location_weather(keyword)



parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()
group.add_argument("-c", "--complete", help="show current HKO weather and all location weather.", action="store_true")
group.add_argument("-n", "--now", help="show current HKO weather.", action="store_true")
group.add_argument("-a", "--all", help="show all location current temp.", action="store_true")
group.add_argument("-s", "--server", help="start a flask server for serving json and xml (Go to http://127.0.0.1:5000 for description)", action="store_true")
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
	elif args.server:
		app.run()
	elif args.forecast == None and len(args.location) > 0:
		c = CurrentWeatherParser()
		d = c.location_weather(args.location)
	elif args.forecast > 0 and args.location == None:
		f = ForecastWeatherParser()
		d = f.forecast(args.forecast)

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
		if not args.server:
			pprint.pprint(d)
		
else:
	parser.print_help()




