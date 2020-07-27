# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pprint import pprint
# from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import os
from urllib.parse import urlparse
import scrapy

class InstaparserPipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.insta_parse

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)


        return item

    def __del__(self):
        self.client.close()


