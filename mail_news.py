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



def pars_mail_news():
    mail_news = []


    link = 'https://news.mail.ru/'
    response = requests.get(link,
                            headers=header)
    dom = html.fromstring(response.text)

    items = dom.xpath("//div[@class='newsitem newsitem_height_fixed js-ago-wrapper']")
    for item in items:
        data = item.xpath("./..//text()")
        url = item.xpath(".//@href")
        time = str(item.xpath('.//@datetime')[0])
        source = data[2]
        for d in range(3, len(data)):
            news = {}
            if d != 4:
                news['name'] = str(data[d]).replace('\xa0', ' ')
                news['link'] = link + str(url[0])
                news['source'] = source
                news['time'] = time
                news['web-site'] = link

                mail_news.append(news)

    news_db.insert_many(mail_news)
    return mail_news

pprint(pars_mail_news())

