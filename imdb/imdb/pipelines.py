# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class ImdbPipeline:
    def process_item(self, item, spider):
        return item


class MoviesPipeline:
    collection_name = "movies"
    
    def open_spider(self, spider):
        self.client = MongoClient("mongodb://localhost:27017")
        db = self.client["ScrapingIMDB"]

        self.movie = db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.movie.insert_one(dict(item))
        return item


class SeriesPipeline:
    collection_name = "series"
    
    def open_spider(self, spider):
        self.client = MongoClient("mongodb://localhost:27017")
        db = self.client["ScrapingIMDB"]

        self.serie = db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.serie.insert_one(dict(item))
        return item

