import pyowm
from datetime import datetime as dt
from cogs import LoginsAndKeys as LaK


owm = pyowm.OWM(LaK.api_keys["owm"])  # You MUST provide a valid API key


def currentTemp():
	# Search for current weather in Dublin
	observation = owm.weather_at_place('Dublin,IE')
	w = observation.get_weather()
	return w.get_temperature('celsius')['temp']

def weatherFor():
	fc = owm.three_hours_forecast('Dublin, IE')
	f = fc.get_forecast()
	emptyList = []
	for weather in f:
		time = weather.get_reference_time(timeformat='date')
		datetime_object = dt.strptime(str(time), '%Y-%m-%d %H:%M:%S+00:00').strftime('%H:%M')
		emptyList.append([datetime_object, weather.get_detailed_status()])
	return emptyList
