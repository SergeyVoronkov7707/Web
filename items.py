# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def val_price(value):
    if value:
        return float(value.replace(' ', ''))
    else:
        return value


def line_photo(value):
    if value[:2] == '//':
        return f'http:{value}'
    else:
        return value


class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=MapCompose(val_price))
    currency = scrapy.Field(output_processor=TakeFirst())
    num = scrapy.Field(output_processor=TakeFirst())
    name_adress = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())

    photos = scrapy.Field(input_processor=MapCompose(line_photo))
    photo_cat = scrapy.Field()
    specific = scrapy.Field()
