# -*- coding: utf-8 -*-

import scrapy
from allris.items import VoItem


class Allris_Vo_spider(scrapy.Spider):
    name = "vo_all"
    allowed_domains = ["ratsinfo.leipzig.de"]
    start_urls = [
        "https://ratsinfo.leipzig.de/bi/vo040.asp?showall=true",
    ]

    def parse(self, response):
        for sel in response.xpath('//tbody/tr'):
            item = VoItem()
            item['id'] = sel.xpath('td/form/input[@type="hidden"]/@value').extract()
            item['name'] = sel.xpath('td/a/text()').extract()
            item['originator'] = sel.xpath('td[@class="text2"][1]/text()').extract()
            item['publishedDate'] = sel.xpath('td[@class="text2"][2]/text()').extract()
            item['paperType'] = sel.xpath('td[@class="text2"][3]/text()').extract()
            item['mainFile'] = sel.xpath('td/a/@href').extract()
            item['body'] = "Stadtrat Leipzig"
            yield item
