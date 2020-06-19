import logging
import scrapy

logger = logging.getLogger(__name__)

class FixWebUrlPipeline(object):
    def process_item(self, item, spider):
        if item.get('web'):
            item['web'] = item['web'].replace('N/A', 'https://ratsinfo.leipzig.de/bi/')
        return item

class AddOriginatorPipeline(object):
    async def process_item(self, item, spider):
        if item['type'] != 'https://schema.oparl.org/1.0/Paper':
            return item
        if not item.get('web'):
            return item

        paper_url = item.get('web')
        logger.info("Add Originator from: {}".format(paper_url))

        request = scrapy.Request(paper_url)
        response = await spider.crawler.engine.download(request, spider)
        if response.status != 200:
            return item

        xpath = '//td[@class="ko1"]/table[@class="tk1"]/tr[descendant::td[contains(.,"Einreicher:")]]/td/text()'
        data = response.xpath(xpath).getall()
        originator = data[1]

        logger.info("Found Originator: {}".format(originator))
        item['leipzig:originator'] = originator

        return item
