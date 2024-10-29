# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeberItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    phrase = scrapy.Field()
    inDict = scrapy.Field()


class OxfordItem(scrapy.Item):
    phrase = scrapy.Field()
    inDict = scrapy.Field()


class GBNCItem(scrapy.Item):
    word = scrapy.Field()
    frequencies = scrapy.Field()
