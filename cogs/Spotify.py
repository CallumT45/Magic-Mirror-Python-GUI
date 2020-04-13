import json
import os
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import time
import datetime

from cogs import LoginsAndKeys as LaK
# import LoginsAndKeys as LaK

username = LaK.logins["spotifyUsername"]
scope = 'user-read-private user-read-playback-state'

SPOTIPY_CLIENT_ID=LaK.api_keys["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET=LaK.api_keys["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI='https://www.google.ie'

def getToken():
	"""Gets a access token for the spotify api, with the access privilages as set out in scope. This token expires in 1 hour"""
	try:
	    token = util.prompt_for_user_token(username, scope,
	     client_id = SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri = SPOTIPY_REDIRECT_URI)
	except (AttributeError, JSONDecodeError):
	    os.remove(f".cache-{username}")
	    token = util.prompt_for_user_token(username, scope,
	    	client_id = SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri = SPOTIPY_REDIRECT_URI)
	return token

def main(token):
	spotifyObject = spotipy.Spotify(auth=token)

	track = spotifyObject.current_user_playing_track()
	trackInfo = json.dumps(track, sort_keys=True, indent=4)
	parsed_json = (json.loads(trackInfo))
	if parsed_json:
		duration = parsed_json['item']['duration_ms']//1000
		current = parsed_json['progress_ms']//1000
		track = parsed_json['item']['name']
		artist = parsed_json['item']['artists'][0]['name']
		duration_full = str(datetime.timedelta(seconds=duration))
		duration_short =  datetime.datetime.strptime(duration_full, '%H:%M:%S').strftime('%M:%S')

		current_full = str(datetime.timedelta(seconds=current))
		current_short =  datetime.datetime.strptime(current_full, '%H:%M:%S').strftime('%M:%S')
		percentage_complete = round(current/duration,2)
		return [track, artist, current_short, duration_short, percentage_complete]

if __name__=="__main__":
	token = getToken()
	print(main(token))
