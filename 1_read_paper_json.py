import scrapy
import scrapy.signals
from scrapy.crawler import CrawlerProcess
from allris.spiders.oparl import OparlSpider
from pathlib import Path

settings = {
    "HTTPCACHE_ENABLED": True,
    "LOG_LEVEL": "INFO",
    "CLOSESPIDER_PAGECOUNT": 5000,
    "ITEM_PIPELINES": {
        "allris.pipelines.leipzig.FixWebUrlPipeline": 200,
        "allris.pipelines.leipzig.AddOriginatorPipeline": 300,
    },
    "FEEDS": {
        Path(".").parent.absolute() / "data" / "%(object_type)s_%(time)s.jl": {"format": "jsonlines"},
    },
}

spargs = {
    "body_url": "https://ratsinformation.leipzig.de/allris_leipzig_public/oparl/bodies?id=2387",
    "allowed_domains": ["ratsinformation.leipzig.de"],
    "object_type": "paper",
    "modified_from": "2023-03-29T00:00:00",
    "modified_to": "2023-04-17T00:00:00",
    "page_from": "1",
    "page_to": "10"
}

process = CrawlerProcess(settings)
process.crawl(OparlSpider, **spargs)
process.start()
