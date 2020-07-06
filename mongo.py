from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client['vacancys_db']

vacancys = db.vacancys

# mail_link = 'https://www.superjob.ru/'
# mail_link = 'https://hh.ru/'
for vc in vacancys.find({'salary_min': {'$gt': 50000}, 'salary_max': {'$lt': 150000}, 'main_url': 'https://hh.ru/'}, {
    'salary_min': 1,
    'salary_max': 1,
    'currency': 1,
    'main_url': 1,
    '_id': 1}):
    print(vc)

# vacancys.delete_many({})
