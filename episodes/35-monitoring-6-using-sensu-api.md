# VM Monitoring #6 - Creating a Python script to use Sensu API

## Using Sensu API to view our events

Instead of using the sensu UI, we will use the sensu api to look at the events

### Authenticate to Sensu API

You can find more information about authenticating to sensu api [here](https://docs.sensu.io/sensu-go/latest/api/)

For now, I am gonna use the username and password to fetch an access token and then use that with our
API calls

```
curl -u 'YOUR_USERNAME:YOUR_PASSWORD' http://sensu-backend-ip:8080/auth

curl -u 'admin:password' http://192.168.33.30:8080/auth
```

This should give you an access token, copy it
These tokens are only valid for 15 minutes, you need to refresh them often


Now we will use the events api to get a list of all the events. More about events api [here](https://docs.sensu.io/sensu-go/latest/api/events/)
```
curl -H "Authorization: Bearer <access_token>" \
http://192.168.33.30:8080/api/core/v2/namespaces/default/events
```


## The script

```
#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth

USERNAME="admin"
PASSWORD="password"
BASE_URL="http://192.168.33.30:8080"

AUTH_URL = BASE_URL + "/auth"
EVENTS_URL = BASE_URL + "/api/core/v2/namespaces/default/events"


r = requests.get(AUTH_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))

access_token = r.json()['access_token']

headers = {
        'Authorization': 'Bearer ' + access_token}

r = requests.get(EVENTS_URL, headers=headers)

data = r.json()

for entry in data:
    #print (entry['check']['metadata']['name'] + "\t" + str(entry['check']['status']) + "\t\t" + entry['check']['output'])
    print("{: <20} {: <20} {: <20}".format(entry['check']['metadata']['name'], str(entry['check']['status']), entry['check']['output']))

```