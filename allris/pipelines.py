# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
# from scrapy.contrib.exporter import JsonItemExporter
from scrapy.contrib.exporter import JsonLinesItemExporter


class AllrisPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        for entry in item.values():
            if not entry:
                raise DropItem("Empty ID in item %s" % item)

        item['id'] = item['id'][0]
        item['name'] = item['name'][0]
        item['reference'] = item['name'].split()[0]
        item['originator'] = item['originator'][0].split(',')
        item['publishedDate'] = item['publishedDate'][0]
        item['paperType'] = item['paperType'][0]
        item['mainFile'] = item['mainFile'][0]
        return item


class JsonExportPipeline(object):

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}

    def spider_opened(self, spider):
        file = open('%s_items.json' % spider.name, 'w+b')
        self.files[spider] = file
        # self.exporter = JsonItemExporter(file)
        self.exporter = JsonLinesItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
