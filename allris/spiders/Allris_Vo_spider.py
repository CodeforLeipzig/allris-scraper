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
            item['location'] = sel.xpath('td/a/@href').extract()
            yield item
