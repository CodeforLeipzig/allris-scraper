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
    fmt_str = r"%Y-%m-%d"  # replaces the fromisoformatm, not available in python 3.6

    def __init__(self, name=None, **kwargs):
        if 'domain' in kwargs:
            self.allowed_domains = [kwargs['domain']]
        if 'page_from' not in kwargs:
            raise ValueError('Missing required argument: "page_from". Got arguments: {}'.format(kwargs))
        if 'modified_from' not in kwargs:
            raise ValueError('Missing required argument: "modifier_from". Got arguments: {}'.format(kwargs))
        self.page_from = kwargs['page_from']
        self.modified_from = datetime.strptime(kwargs['modified_from'], self.fmt_str)
        if 'page_to' in kwargs:
            self.page_to = kwargs['page_to']
        if 'modified_to' in kwargs:
            self.modified_to = datetime.strptime(kwargs['modified_to'], self.fmt_str)
        self.first = True
        if 'body_url' not in kwargs:
            raise ValueError('Missing required argument: "body_url". Got arguments: {}'.format(kwargs))
        super(OparlSpider, self).__init__(name, **kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.body_url, callback=self.parse_body)

    def parse_body(self, response):
        self.logger.info("Parsing Body: %s" % response.url)
        document = json.loads(response.text)

        if not document.get('type') == 'https://schema.oparl.org/1.1/Body':
            raise ValueError('Not a document of type Body: {}'.format(response.url))

        list_url = self.fix_url(document[self.object_type])
        self.logger.info("list_url {}".format(list_url))
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        self.logger.info("Parsing Object List: %s" % response.url)
        document = json.loads(response.text)

        total_item_count = 0
        processed_item_count = 0

        for item in document['data']:
            total_item_count += 1
            item_modified = item['date'] if 'date' in item else None
            if item_modified is not None:
                item_modified_parsed = datetime.strptime(item_modified.split("+")[0], self.fmt_str)
                if item_modified_parsed < datetime.strptime(self.modified_from, self.fmt_str):
                    self.logger.info("skipping at date {} < modified_from {}".format(item_modified, self.modified_from))
                else:
                    if self.modified_to is not None and item_modified_parsed > datetime.strptime(self.modified_to,
                                                                                                 self.fmt_str):
                        self.logger.info("skipping at date {} > modified_to {}".format(item_modified, self.modified_to))
                    else:
                        processed_item_count += 1
                        yield item
            else:
                self.logger.info("item has no field date, thus skipping")

        next_url = document['links'].get('next')
        self.logger.info("next_url {}".format(next_url))

        fixed = furl(next_url)
        next_page = fixed.args['page']
        self.logger.info("next_page {}".format(next_page))

        if processed_item_count == 0:
            self.logger.info("stopping before page {} as nothing processed at the current page".format(next_page))
            return

        if int(next_page) < int(self.page_from):
            self.logger.info("stopping at page {} < page_from {}".format(next_page, self.page_from))
            return
        if self.page_to is not None and int(next_page) > int(self.page_to):
            self.logger.info("stopping at page {} > page_to {}".format(next_page, self.page_to))
            return

        if next_url is not None:
            self.first = False
            yield scrapy.Request(url=next_url, callback=self.parse_list)

    def fix_url(self, url):
        fixed = furl(url)
        if self.first:
            fixed.args['page'] = self.page_from
        return str(fixed)
