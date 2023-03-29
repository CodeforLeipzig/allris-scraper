# -*- coding: utf-8 -*-
import scrapy
import json
import re

class PapersSpider(scrapy.Spider):
    name = 'papers'
    allowed_domains = ['ratsinformation.leipzig.de']
    start_urls = ['https://ratsinformation.leipzig.de/allris_leipzig_public/oparl/papers?body=2387']

    # limit the number of scraped pages for now
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 6
    }

    def parse(self, response):
        self.logger.info('Parsing page: %s', response.url)
        page = json.loads(response.text)

        papers = page['data']
        for paper in papers:
            yield paper

        next_url = page['links'].get('next')
        if next_url is not None:
            yield scrapy.Request(url=next_url, callback=self.parse)
