# -*- coding: utf-8 -*-
import scrapy
import json
import re

class MeetingsSpider(scrapy.Spider):
    name = 'meetings'
    allowed_domains = ['ratsinfo.leipzig.de']
    # only scraping "Ratsversammlung" for now
    start_urls = ['https://ratsinfo.leipzig.de/bi/oparl/1.0/meetings.asp?organization=2387']

    def parse(self, response):
        self.logger.info('Parsing page: %s', response.url)
        page = json.loads(response.text)

        meetings = page['data']
        for meeting in meetings:
            yield meeting

        next_url = page['links'].get('next')
        if next_url is not None:
            yield scrapy.Request(url=next_url, callback=self.parse)
