# -*- coding: utf-8 -*-
import scrapy
import json
import re


class MeetingsSpider(scrapy.Spider):
    name = "meetings"
    allowed_domains = ["ratsinformation.leipzig.de"]

    def start_requests(self):
        url = getattr(
            self,
            "start_url",
            "https://ratsinformation.leipzig.de/allris_leipzig_public/oparl/meetings?body=2387",
        )
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info("Parsing page: %s", response.url)
        page = json.loads(response.text)

        meetings = page["data"]
        for meeting in meetings:
            yield meeting

        next_url = page["links"].get("next")
        if next_url is None:
            self.last_url = response.url
        else:
            yield scrapy.Request(url=next_url, callback=self.parse)

