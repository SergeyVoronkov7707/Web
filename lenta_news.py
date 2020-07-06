from pprint import pprint
from lxml import html
import requests

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['ya_news']
news_db = db.ya_news

# news_db.delete_many({})
header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Accept': '*/*'}



def pars_lenta_news():
    lenta_news = []


    link = 'https://lenta.ru'
    response = requests.get(link,
                            headers=header)
    dom = html.fromstring(response.text)

    items = dom.xpath("//a[@href]")
    for item in items:
        if len(item.xpath('./time')) != 0:
            name = str(item.xpath('./text()')[0])
            name = name.replace('\xa0', ' ')
            time = str(item.xpath('./time/@datetime')[0])
            news = {}

            url = item.xpath("./@href")

            news['name'] = name
            if str(link[0]).find('http') == -1:
                news['link'] = link + str(url[0])
            else:
                news['link'] = str(link[0])

            news['source'] = link
            news['time'] = time
            news['web-site'] = link

            lenta_news.append(news)



    news_db.insert_many(lenta_news)
    return (lenta_news)

pprint(pars_lenta_news())

