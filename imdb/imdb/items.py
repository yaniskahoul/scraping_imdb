# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    title = scrapy.Field()
    original_title = scrapy.Field()
    score = scrapy.Field()
    genre = scrapy.Field()
    date = scrapy.Field()
    durée = scrapy.Field()
    description = scrapy.Field()
    acteurs = scrapy.Field()
    public = scrapy.Field()
    pays = scrapy.Field()
    

    

