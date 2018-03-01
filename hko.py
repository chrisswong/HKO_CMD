import argparse
import pprint

from flask import Flask 
from flask import jsonify
from flask import Response
from flask import render_template
from WeatherManager import WeatherManager

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
	manager = WeatherManager()
	return handle_format(manager.now(), format)

@app.route('/complete/<format>')
def complete(format):
	manager = WeatherManager()
	return handle_format(manager.complete(), format)

@app.route('/all/<format>')
def all(format):
	manager = WeatherManager()
	return handle_format(manager.all_location(), format)

@app.route('/forecast9Days/<format>')
def forecast9Days(format):
	manager = WeatherManager()
	return handle_format(manager.forecast(), format)

@app.route('/forecast/<int:num_of_days>/<format>')
def forecast(num_of_days, format):
	manager = WeatherManager()
	return handle_format(manager.forecast(num_of_days), format)

@app.route('/location/<keyword>/<format>')
def location(keyword, format):
	manager = WeatherManager()
	return handle_format(manager.location(keyword), format)

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')



parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()
group.add_argument("-c", "--complete", help="show current HKO weather and all location weather.", action="store_true")
group.add_argument("-n", "--now", help="show current HKO weather.", action="store_true")
group.add_argument("-a", "--all-location", help="show all locations' weather.", action="store_true")
group.add_argument("-l", "--location", help="show specific location's current weather. shows all no location name specific.")
group.add_argument("-f", "--forecast", help="show upcoming [1-9] days forecast. ", type=int)


group.add_argument("-s", "--server", help="start a flask server for serving json and xml (Go to http://127.0.0.1:5000 for description)", action="store_true")


parser.add_argument("-v", "--verbose", help="show debug message")
parser.add_argument("-o", "--output", choices=['xml','json'], help="output as selected file format")

args = parser.parse_args()

if any(vars(args).values()):
	d = dict()
	manager = WeatherManager()
	if args.complete:
		d = manager.complete()
	elif args.now: 
		d = manager.now()
	elif args.all_location:
		d = manager.all_location()
	elif args.server:
		app.run()
	elif args.forecast == None:
		d = manager.location(args.location)
	elif args.forecast > 0 and args.location == None:
		d = manager.forecast(args.forecast)

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