import json
import requests
import config
from pprint import pprint

main_link = 'https://www.googleapis.com/youtube/v3/channels'

key = config.key
params = {'key': key, 'part': 'snippet', 'contentDetails':'statistics','forUsername': 'GoogleDevelopers'}

response = requests.get(main_link, params=params)
data = response.json()
pprint(data)

with open('youresponse.json', 'w') as f:
    json.dump(data, f)
