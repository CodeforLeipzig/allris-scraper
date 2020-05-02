import scrapy
import scrapy.signals
from scrapy.crawler import CrawlerProcess
from allris.spiders.oparl import OparlSpider

def spider_closed(spider, reason):
    pass

settings = {
    'HTTPCACHE_ENABLED': True,
    'LOG_LEVEL': 'INFO',
    'FEED_FORMAT': 'jsonlines',
    'FEED_URI': 'stdout:'
}
process = CrawlerProcess(settings)

spargs = {
    'body_url': 'https://ratsinfo.leipzig.de/bi/oparl/1.0/bodies.asp?id=2387',
    'allowed_domains': ['ratsinfo.leipzig.de'],
    'object_type': 'meeting',
    'since': '2020-04-01T00:00:00'
}
process.crawl(OparlSpider, **spargs)

for p in process.crawlers:
    p.signals.connect(spider_closed, signal=scrapy.signals.spider_closed)


process.start()
