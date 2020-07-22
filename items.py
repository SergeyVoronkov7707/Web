# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    user_id = scrapy.Field()
    photo_subscription = scrapy.Field()
    id_subscription = scrapy.Field()
    name_subscription = scrapy.Field()
    section = scrapy.Field()
    pass
