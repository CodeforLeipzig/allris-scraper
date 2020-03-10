import scrapy
import scrapy.signals
from scrapy.crawler import CrawlerProcess
from allris.spiders.oparl import OparlSpider
from pathlib import Path

settings = {
    'HTTPCACHE_ENABLED': True,
    'LOG_LEVEL': 'INFO',
    'CLOSESPIDER_PAGECOUNT': 2,
    'ITEM_PIPELINES': {
        'allris.pipelines.leipzig.FixWebUrlPipeline': 200,
        'allris.pipelines.leipzig.AddOriginatorPipeline': 300
    },
    'FEED_FORMAT': 'jsonlines',
    # 'FEED_URI': 'stdout:'
    'FEED_URI': Path('.') / 'data' / '%(object_type)s_%(time)s.jl'
}

spargs = {
    'body_url': 'https://ratsinfo.leipzig.de/bi/oparl/1.0/bodies.asp?id=2387',
    'allowed_domains': ['ratsinfo.leipzig.de'],
    'object_type': 'paper',
    'since': '2020-04-01T00:00:00'
}

process = CrawlerProcess(settings)
process.crawl(OparlSpider, **spargs)
process.start()
