# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VoItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    type = scrapy.Field()
    body = scrapy.Field()
    name = scrapy.Field()
    reference = scrapy.Field()
    publishedDate = scrapy.Field()
    paperType = scrapy.Field()
    mainFile = scrapy.Field()
    location = scrapy.Field()
    originator = scrapy.Field()
    consultation = scrapy.Field()
    modified = scrapy.Field()
