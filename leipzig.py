import scrapy
import scrapy.signals
from scrapy.crawler import CrawlerProcess
from allris.spiders.oparl import OparlSpider
from pathlib import Path
import json
import requests as re
from pathlib import Path

settings = {
    "HTTPCACHE_ENABLED": True,
    "LOG_LEVEL": "INFO",
    "CLOSESPIDER_PAGECOUNT": 2,
    "ITEM_PIPELINES": {
        "allris.pipelines.leipzig.FixWebUrlPipeline": 200,
        "allris.pipelines.leipzig.AddOriginatorPipeline": 300,
    },
    "FEED_FORMAT": "jsonlines",
    # 'FEED_URI': 'stdout:'
    "FEED_URI": Path(".").parent.absolute() / "data" / "%(object_type)s_%(time)s.jl",
}

spargs = {
    "body_url": "https://ratsinfo.leipzig.de/bi/oparl/1.0/bodies.asp?id=2387",
    "allowed_domains": ["ratsinfo.leipzig.de"],
    "object_type": "paper",
    "since": "2020-04-01T00:00:00",
}

# looks up all .jl files in the data folder and downloads the pdf linked under mainFile/accessUrl
def download_pdfs():
    pathlist = Path("data/").glob("**/*.jl")
    for path in pathlist:
        jl_file = str(path)
        with open(jl_file, "r") as f:
            for paper in f:
                paper_json = json.loads(paper)
                if not paper_json.get("mainFile") or not paper_json.get("mainFile").get(
                    "accessUrl"
                ):  # manche von den jsons haben kein pdf als mainFile verlinkt – sollte man es da woanders suchen?
                    continue
                pdf_name = paper_json["mainFile"]["fileName"]
                pdf_path = Path(f"data/pdfs/{pdf_name}")
                if not pdf_path.is_file():
                    pdf_url = paper_json["mainFile"]["accessUrl"]
                    response = re.get(pdf_url)
                    Path("data/pdfs").mkdir(parents=True, exist_ok=True)
                    with open(f"data/pdfs/{pdf_name}", "wb") as f:
                        f.write(response.content)


process = CrawlerProcess(settings)
process.crawl(OparlSpider, **spargs)
process.start()
download_pdfs()
