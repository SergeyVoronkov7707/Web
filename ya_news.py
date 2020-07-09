from pprint import pprint
from lxml import html
import requests
from datetime import date, timedelta
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['ya_news']
news_db = db.ya_news

# news_db.delete_many({})
header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Accept': '*/*'}


n = 0
def pars_ya_news():
    ya_news = []


    link = 'https://yandex.ru/news'
    response = requests.get(link,
                            headers=header)
    dom = html.fromstring(response.text)

    items = dom.xpath("//h2[@class='story__title']/a/../../../..")
    for item in items:
        news = {}
        data = item.xpath(".//text()")
        url =item.xpath(".//@href")
        dtime = str(date.today())
        ydtime = str(date.today() - timedelta(days=1))

        if len(data) == 1:
            name = data[0]
            source = data[1][:-6]
            time = data[1][-5:]
        else:
            time = data[len(data) - 3][-5:]
            source = data[len(data) - 3][:-6]
            name = ''
            for i in range(len(data) - 3):
                name = name + str(data[i])

        if source.find("вчера") != -1:
            source = source[:-11]
            time = ydtime + ' ' + time
        else:
            time = dtime + ' ' + time


        news['name'] = name
        news['url'] =str(url[0])
        news['source'] = source
        news['time'] = time

        ya_news.append(news)
    news_db.insert_many(ya_news)
    return news_db







# pprint(pars_ya_news())

