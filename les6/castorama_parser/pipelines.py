# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from spiders.castorama_ru import CastoramaRuSpider
from pymongo import MongoClient
# from scrapy.utils.python import to_bytes


class CastoramaParserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.db_castorama

    def process_item(self, item, spider):
        if item:
            item['name'] = item['name'].replace('\n', '').strip()
            # item['price'] = int(item['price'].replace(' ', ''),)
            collection = self.mongo_base[spider.name]
            collection.insert_one(item)
        return item


class PhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for img in item['images']:
                try:
                    yield scrapy.Request(CastoramaRuSpider.url + img)

                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['images'] = [itm[1] for itm in results if itm[0]]
        return item