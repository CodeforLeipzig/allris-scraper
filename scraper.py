import os
os.environ['SCRAPERWIKI_DATABASE_NAME'] = 'sqlite:///data.sqlite'
import scraperwiki

import scrapy
import scrapy.signals
from scrapy.crawler import CrawlerProcess
from allris.spiders.meetings import MeetingsSpider

def item_scraped(item, response, spider):
    record = dict((k, item[k]) for k in ('id', 'name', 'start', 'end', 'web'))
    scraperwiki.sql.save(['id'], record, table_name='data')

def spider_closed(spider, reason):
    # close pending transactions
    scraperwiki.sql.commit_transactions()
    # save the last url scraped
    last_url = getattr(spider, 'last_url', '')
    scraperwiki.sql.save_var('last_url', last_url)

def get_start_url():
    start_url = 'https://ratsinformation.leipzig.de/allris_leipzig_public/oparl/meetings?body=2387&p=100'        
    start_url = os.getenv('MORPH_START_URL') or scraperwiki.sql.get_var('last_url')
    return start_url

def setup():
    settings = { 'HTTPCACHE_ENABLED': True, 'LOG_LEVEL': 'INFO'}
    process = CrawlerProcess(settings)
    process.crawl(MeetingsSpider, start_url=get_start_url())
    for p in process.crawlers:
        p.signals.connect(item_scraped, signal=scrapy.signals.item_scraped)
        p.signals.connect(spider_closed, signal=scrapy.signals.spider_closed)
    return process

runner = setup()
runner.start()
