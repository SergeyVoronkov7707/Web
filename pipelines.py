# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pprint import pprint


class JobparserPipeline:

    def __init__(self):
        self.client = MongoClient('localhost',27017)
        self.mongo_base = self.client.vacansy123

    def process_sj(self,item, spider):
        pass
    def process_item(self, item, spider):
        job_parse = {}
        collection = self.mongo_base[spider.name]

        if spider.name == 'hhru':
            salary = item['salary']
            res = []
            sal_max = []
            sal_min = []
            currency = []
            if str(salary).find('руб'):
                item['currency'] = 'руб'
            elif str(salary).find('EUR'):
                item['currency'] = 'EUR'
            elif str(salary).find('USD'):
                item['currency'] = 'USD'
            else:
                pass

            for i in salary:
                try:
                    int(i[0])
                    t = i.split()
                    t = t[0] + t[1]
                    res.append(int(t))
                except:
                    pass
            try:
                sal_min.append(res[0])
                sal_max.append(res[1])
                job_parse['name'] = item['name']
                if len(item['salary']) < 5 and item['salary'][0] == 'от':
                    item['salary_min'] = sal_min
                if len(item['salary']) < 5 and item['salary'][0] == 'до':
                    item['salary_max'] = sal_min
                item['salary_min'] = sal_min
                item['salary_max'] = sal_max
                item['currency'] = currency
                item['line'] = spider.name


                # del item['salary']


            except:
                pass
            del item['salary']
            pprint(item)
            collection.insert_one(item)
            return item
        if spider.name == 'sjru':
            item['line'] = spider.name
            collection.insert_one(item)
            pprint(item)

          

    def __del__(self):
        self.client.close()



