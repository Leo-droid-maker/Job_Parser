# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient, ASCENDING
from pymongo.errors import *


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongobase = client.vacancies_from_scrapy

    def process_item(self, item, spider):

        match spider.name:
            case 'hhru':
                try:
                    item['min'], item['max'], item['cur'] = self.hhru_salary_handler(item)
                except UnboundLocalError:
                    pass
            case 'superjobru':
                try:
                    item['min'], item['max'], item['cur'] = self.superjobru_salary_handler(item)
                except UnboundLocalError:
                    pass

        collection = self.mongobase[spider.name]
        collection.create_index([("link", ASCENDING)], name="vacancy_link_index", unique=True)
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            print(f'Данный элемент уже есть в базе данных: {item["name"]}')

        return item

    def hhru_salary_handler(self, item):
        try:
            match item['salary']:
                case (_, min_comp, _, max_comp, _, currency, _):
                    min, max, cur = \
                        int(min_comp.replace(u"\xa0", '')), \
                        int(max_comp.replace(u"\xa0", '')), \
                        currency
                case (pref, comp, _, currency, _) if pref == 'от':
                    min, max, cur = int(comp.replace(u"\xa0", '')), None, currency
                case (pref, comp, _, currency, _) if pref == 'до':
                    min, max, cur = None, int(comp.replace(u"\xa0", '')), currency

        except:
            min = None
            max = None
            cur = None

        del item['salary']
        return min, max, cur

    def superjobru_salary_handler(self, item):
        try:
            match item['salary']:
                case (min_comp, _, _, _, max_comp, _, currency):
                    min, max, cur = \
                        int(min_comp.replace(u"\xa0", '')), \
                        int(max_comp.replace(u"\xa0", '')), \
                        currency.replace('.', '')
                case (pref, _, comp) if pref == 'от':
                    min, max, cur = int((comp.replace(u"\xa0", '')).replace('руб.', '')), None, 'руб'
                case (pref, _, comp) if pref == 'до':
                    min, max, cur = None, int((comp.replace(u"\xa0", '')).replace('руб.', '')), 'руб'
                case 'По договорённости':
                    min = None
                    max = None
                    cur = None

        except:
            min = None
            max = None
            cur = None

        del item['salary']

        return min, max, cur
