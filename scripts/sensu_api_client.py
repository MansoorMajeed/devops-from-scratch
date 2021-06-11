#!/usr/bin/env python3

import requests

from requests.auth import HTTPBasicAuth

USERNAME = 'admin'
PASSWORD = 'password'

BASE_URL = 'http://192.168.33.30:8080'

AUTH_URL = BASE_URL + '/auth'
EVENTS_URL = BASE_URL + '/api/core/v2/namespaces/default/events'

r = requests.get(AUTH_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))

access_token = r.json()['access_token']


headers = {
        'Authorization': 'Bearer ' + access_token
    }


r = requests.get(EVENTS_URL, headers=headers)

resp = r.json()

for entry in resp:
    print("{: <20} {: <20} {: <20}".format(entry['check']['metadata']['name'],  str(entry['check']['status']), entry['check']['output']))






