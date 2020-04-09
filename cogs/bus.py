import requests
import json

def main(stopid):
    URL = 'https://data.smartdublin.ie/cgi-bin/rtpi/'
    uri_extens = 'realtimebusinformation'
    req_items = {'stopid': str(stopid)}

    resp = requests.get(URL + uri_extens, params=req_items)
    parsed_json = (json.loads(resp.text))
    emptyList = []
    for i in range(parsed_json['numberofresults']):
    	emptyList.append([parsed_json['results'][i]['route'], parsed_json['results'][i]['destination'], parsed_json['results'][i]['duetime']])
    return emptyList

#This is data from the smart dublin api, the api has many other features. A full wrapper can be found 
#at https://github.com/theelous3/DB_PAW-Dublin-Bus-Python-API-Wrapper.