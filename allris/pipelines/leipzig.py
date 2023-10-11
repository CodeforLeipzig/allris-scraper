import logging
import scrapy

logger = logging.getLogger(__name__)


class FixWebUrlPipeline(object):
    def process_item(self, item, spider):
        if item.get("web"):
            item["web"] = item["web"].replace("N/A", "https://ratsinformation.leipzig.de/bi/")
        return item


class AddOriginatorPipeline(object):
    async def process_item(self, item, spider):
        if item["type"] != "https://schema.oparl.org/1.1/Paper":
            return item
        if not item.get("web"):
            return item

        paper_url = item.get("web")
        logger.info("Add Originator from: {}".format(paper_url))

        request = scrapy.Request(paper_url)
        response = await spider.crawler.engine.download(request)
        if response.status != 200:
            return item

        xpath = "//span[@id='vofamt']/text()"
        data = response.xpath(xpath).getall()
        if data != null and length(data) > 0:
            originator = data[0]
            logger.info("Found Originator: {}".format(originator))
            item["leipzig:originator"] = originator
        else:
            logger.info("Found no originator")
            item["leipzig:originator"] = "Unbekannt"

        return item
