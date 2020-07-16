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
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.vacansy123

    def process_item(self, item, spider):
        salary = item['salary']
        if spider.name == 'hhru':
            item['salary_min'], item['salary_max'], item['currency'] = self.hh_process_salary(salary)
        elif spider.name == 'sjru':
            item['salary_min'], item['salary_max'], item['currency'] = self.sj_process_salary(salary)
        salary_min = item['salary_min']
        salary_max = item['salary_max']
        salary_cur = item['currency']
        item['line'] = spider.name

        del item['salary']
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        pprint(item)
        return item
    
    def __del__(self):
        self.client.close()

    def hh_process_salary(self, salary):
        res = []
        try:
            if len(salary) == 7:
                for item in salary:
                    if item[0].isdigit():
                        sal = int(str(item).replace('\xa0', ''))
                        res.append(sal)
                sal_min = res[0]
                sal_max = res[1]
                currency = salary[-2]
                return sal_min, sal_max, currency
            if len(salary) == 5:
                for item in salary:
                    if item[0].isdigit():
                        sal = int(str(item).replace('\xa0', ''))
                        res.append(sal)
                if salary[0] == 'от':
                    sal_min = res
                    currency = salary[-2]
                    return sal_min, None, currency
                if salary[0] == 'до':
                    sal_max = res
                    currency = salary[-2]
                    return None, sal_max, currency
            else:
                return None, None, None

        except:
            pass

    

    def sj_process_salary(self, salary):
        res = []
        try:
            if salary[0] == 'от':
                sal_min = int(salary[2][:7].replace('\xa0', ''))
                currency = salary[2][7:]
                return sal_min, None, currency
            if salary[0] == 'до':
                sal_max = int(salary[2][:7].replace('\xa0', ''))
                currency = salary[2][7:]
                return None, sal_max, currency
            if len(salary) == 1:
                currency = 'по договоренности'
                return None, None, currency
            if len(salary) == 4:
                for i in salary:
                    fd = i.replace('\xa0', '')
                    res.append(fd)
                sal_min = res[0]
                sal_max = res[1]
                currency = salary[-1]
                return sal_min, sal_max, currency
            else:
                return None, None, None
        except:
            pass
