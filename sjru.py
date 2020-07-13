import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response:HtmlResponse):

        next_page = response.css('a.f-test-button-dalshe::attr(href)').extract_first()


        vacansy_links = response.css('a._6AfZ9::attr(href)').extract()
        for link in vacansy_links:
            yield response.follow(link, callback=self.vacansy_parse)

        yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        name_vac = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract()
        salary = response.xpath("//span[@class='_3mfro _2Wp8I PlM3e _2JVkc']/text()").extract()
        url = response.url
        yield JobparserItem(name=name_vac, salary=salary, url=url)
