from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leruaparser import settings
from leruaparser.spiders.leruaru import LeruaruSpider


if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeruaruSpider, search= 'краска')


    process.start()

