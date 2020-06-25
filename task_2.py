# AIzaSyAPBPZIszn4zioqSsqjk7cHKIC7YZXR4cI


import json
import requests
from pprint import pprint

main_link = 'https://www.googleapis.com/youtube/v3/subscriptions'


user = 'SergeyVoronkov7707'
key = 'AIzaSyAPBPZIszn4zioqSsqjk7cHKIC7YZXR4cI'

params = {'key': key, 'part': 'snippet', 'categoryId': 'Video'}

response = requests.get(main_link, params=params)
data = response.json()
pprint(data)
# log_web = requests.get('https://www.googleapis.com/youtube/v3/subscriptions')


# repo = []
#
# js = log_web.json()
#
# if len(js) != 0:
#     print("Список репозиториев пользователя:")
# else:
#     print("У пользователя нет репозиториев.")
#
# for js_i in js:
# #Отобраны репозитории в котрых пользователь является владельцем
#     if js_i['owner']['login'] == user:
#         repo.append(js_i['name'])
#         print(f"{len(repo)}. {js_i['name']}")
#         with open('gittext.json', 'w') as f:
#             json.dump(repo, f)