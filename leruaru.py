import scrapy
from leruaparser.items import LeruaparserItem
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader


class LeruaruSpider(scrapy.Spider):
    name = 'leruaru'
    allowed_domains = ['leroymerlin.ru']


    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}&suggest=true']

    def parse(self, response:HtmlResponse):
        # next_page = response.xpath("//a[@class='paginator-button next-paginator-button']['href']").extract_first
        # next_page = response.xpath("//a[@class='green-button btn plp-card-list__show-more-btn']").extract_first
        next_page = response.css('a.paginator-button.next-paginator-button::attr(href)').extract_first()

        ads_links = response.xpath("//div[@class='ui-product-card']/div/div[@class='product-name']/a")
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

        yield response.follow(next_page, callback=self.parse)

    def parse_ads(self, response:HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_css('name','h1::text')
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('currency', "//span[@slot='currency']/text()")
        loader.add_xpath('num', "//span[@slot='unit']/text()")
        loader.add_value('url',response.url)
        loader.add_xpath('photos',"//picture/img[@alt='product image']/@src")
        yield loader.load_item()

