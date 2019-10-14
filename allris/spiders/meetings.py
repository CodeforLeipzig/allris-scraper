# -*- coding: utf-8 -*-
import scrapy
import json


class MeetingsSpider(scrapy.Spider):
    name = 'meetings'
    allowed_domains = ['ratsinfo.leipzig.de']
    start_urls = ['https://ratsinfo.leipzig.de/bi/oparl/1.0/meetings.asp?body=2387']

    def parse(self, response):
        meetings = json.loads(response.text)['data']
        for meeting in meetings:
            yield {
                'id': meeting['id'],
                'organization': meeting['organization'],
                'start': meeting['start'],
                'end': meeting['end']
            }
