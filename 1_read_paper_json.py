import os
import sys
import argparse
import datetime
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
}

parser = argparse.ArgumentParser(description='Vorlagen aus dem Leipziger Stadtrat prozessieren')

params = [
    {
        "command_arg": "modified_from",
        "env_arg": "MODIFIED_FROM",
        "spider_arg": "modified_from",
        "default": "2023-01-01T00:00:00",
        "help": "erfasst nur Vorlagen, die nach einschießlich dem angegebenen Datum modifiziert worden sind, default 2023-01-01T00:00:00, bricht den kompletten Erfassungsprozess ab, wenn eine ältere Vorlage gefunden wird"
    },
    {
        "command_arg": "modified_to",
        "env_arg": "MODIFIED_TO",
        "spider_arg": "modified_to",
        "default": (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT00:00:00"),
        "help": "erfasst nur Vorlagen, die vor einschießlich dem angegebenen Datum modifiziert worden sind, default Datum vom morgigen Tag"
    },
    {
        "command_arg": "page_from",
        "env_arg": "PAGE_FROM",
        "spider_arg": "page_from",
        "default": 1,
        "help": "erfasst nur Vorlagen, die auf Seiten größergleich der angegebenen stehen (jeweils 20 Vorlagen pro Seite), default 1"
    },
    {
        "command_arg": "page_to",
        "env_arg": "PAGE_TO",
        "spider_arg": "page_to",
        "default": 10,    
        "help": "erfasst nur Vorlagen, die auf Seiten kleinergleich der angegebenen stehen (jeweils 20 Vorlagen pro Seite), default 10"
    }
]

for entry in params:
    parser.add_argument('--' + entry['command_arg'], 
                        dest=entry['spider_arg'], 
                        action='store',
                        default=entry['default'],
                        help=entry['help'])

args = parser.parse_args()

parsed = {
    "modified_from": args.modified_from,
    "modified_to": args.modified_to,
    "page_from": args.page_from,
    "page_to": args.page_to
}

for entry in params:
    key = entry['command_arg']
    env_key = entry['env_arg']
    value = parsed[key]
    if value is not None:
        spargs[key] = value
    elif env_key in os.environ:
        spargs[key] = os.environ[env_key]


process = CrawlerProcess(settings)
crawler = process.create_crawler(OparlSpider)
process.crawl(crawler, **spargs)
process.start()

failed = crawler.stats.get_value('log_count/ERROR')
if failed:
    sys.exit(1)
