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
        meetings = json.loads(response.text)['data']
        for meeting in meetings:

            agenda_items = []
            for agenda_item in meeting['agendaItem']:
                item = {
                    'id': agenda_item['id'],
                    'type': agenda_item['type'],
                    'number': agenda_item['number'],
                    'name': agenda_item['name']
                }
                agenda_items.append(item)

            # TODO move to pipeline
            meeting['web'] = self.fix_web_link(meeting)

            yield {
                'id': meeting['id'],
                'type': meeting['type'],
                'name': meeting['name'],
                'organization': meeting['organization'],
                'start': meeting['start'],
                'end': meeting['end'],
                'web': meeting['web'],
                'created': meeting['created'],
                'modified': meeting['modified'],
                'agendaItem': agenda_items
            }

    def fix_web_link(self, meeting):
        partial = meeting['web']
        base_url = 'https://ratsinfo.leipzig.de/bi/'
        return re.sub('N/A', base_url, partial)
