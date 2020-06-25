"""
1. Посмотреть документацию к API GitHub,
разобраться как вывести список репозиториев
для конкретного пользователя, сохранить JSON-вывод в файле *.json.
"""

import json
import requests

user = 'SergeyVoronkov7707'

login = requests.get('https://api.github.com/users/' + user + '/repos')

repo = []

js = login.json()

if len(js) != 0:
    print("Список репозиториев пользователя:")
else:
    print("У пользователя нет репозиториев.")

for js_i in js:
    # Отобраны репозитории в котрых пользователь является владельцем
    if js_i['owner']['login'] == user:
        repo.append(js_i['name'])
        print(f"{len(repo)}. {js_i['name']}")
        with open('gittext.json', 'w') as f:
            json.dump(repo, f)
