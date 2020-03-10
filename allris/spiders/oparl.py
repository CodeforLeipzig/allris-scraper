# -*- coding: utf-8 -*-
import scrapy
import json
from furl import furl
from datetime import datetime

class OparlSpider(scrapy.Spider):
    name = 'oparl'

    # these must be set as kwargs to the spider
    allowed_domains = []
    body_url = ''
    object_type = ''

    def __init__(self, name=None, **kwargs):
        if 'domain' in kwargs:
            self.allowed_domains = [kwargs['domain']]
        if 'since' not in kwargs:
            raise ValueError('Missing required argument: "since". Got arguments: {}'.format(kwargs))
        fmt_str =  r"%Y-%m-%dT%H:%M:%S" # replaces the fromisoformatm, not available in python 3.6
        self.since = datetime.strptime(kwargs['since'], fmt_str)
        if 'body_url' not in kwargs:
            raise ValueError('Missing required argument: "body_url". Got arguments: {}'.format(kwargs))
        super(OparlSpider, self).__init__(name, **kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.body_url, callback=self.parse_body)

    def parse_body(self, response):
        self.logger.info("Parsing Body: %s" % response.url)
        document = json.loads(response.text)

        if not document.get('type') == 'https://schema.oparl.org/1.0/Body':
            raise ValueError('Not a document of type Body: {}'.format(response.url))

        list_url = self.fix_url(document[self.object_type])
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        self.logger.info("Parsing Object List: %s" % response.url)
        document = json.loads(response.text)

        for item in document['data']:
            yield item

        next_url = document['links'].get('next')
        if next_url is not None:
            next_url = self.fix_url(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse_list)

    # append modified_since parameter; pagination links fail to include it
    def fix_url(self, url):
        fixed = furl(url)
        fixed.args['modified_since'] = self.since
        return str(fixed)
