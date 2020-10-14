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
    "CLOSESPIDER_PAGECOUNT": 400,
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

# if the paramater jl_file equals "all", the function looks up all .jl files in the data folder and downloads the pdf linked under mainFile/accessUrl. If it is given a .jl file name, it will download all PDF files for that .jl file.
def download_pdfs(jl_file):
    if jl_file == "all":
        pathlist = Path("data/").glob("**/*.jl")
        for path in pathlist:
            jl_file = str(path)
            with open(jl_file, "r") as f:
                for paper in f:
                    paper_json = json.loads(paper)
                    if not paper_json.get("mainFile") or not paper_json.get(
                        "mainFile"
                    ).get(
                        "accessUrl"
                    ):  # manche von den jsons haben kein pdf als mainFile verlinkt – sollte man es da woanders suchen?
                        continue
                    pdf_name = paper_json["mainFile"]["fileName"]
                    pdf_path = Path(f"data/pdfs/{pdf_name}")
                    if not pdf_path.is_file():
                        print("Processing " + f"data/pdfs/{pdf_name}")
                        pdf_url = paper_json["mainFile"]["accessUrl"]
                        response = re.get(pdf_url)
                        Path("data/pdfs").mkdir(parents=True, exist_ok=True)
                        with open(f"data/pdfs/{pdf_name}", "wb") as f:
                            print("Writing contents to " + f"data/pdfs/{pdf_name}")
                            f.write(response.content)
        print("finished!")

    else:
        pathlist = Path("data/").glob("**/*.jl")
        found = False
        for path in pathlist:
            if jl_file == str(path).split("/")[-1]:
                found = True
                with open(str(path), "r") as f:
                    first_file = True
                    for paper in f:
                        paper_json = json.loads(paper)
                        if not paper_json.get("mainFile") or not paper_json.get(
                            "mainFile"
                        ).get(
                            "accessUrl"
                        ):  # manche von den jsons haben kein pdf als mainFile verlinkt – sollte man es da woanders suchen?
                            continue
                        pdf_name = paper_json["mainFile"]["fileName"]
                        pdf_path = Path(f"data/pdfs/{pdf_name}")
                        if not pdf_path.is_file():
                            if not first_file:
                                print("Going to next file..")
                            first_file = False
                            print("Processing " + f"data/pdfs/{pdf_name}")
                            pdf_url = paper_json["mainFile"]["accessUrl"]
                            response = re.get(pdf_url)
                            Path("data/pdfs").mkdir(parents=True, exist_ok=True)
                            with open(f"data/pdfs/{pdf_name}", "wb") as f:
                                print("Writing contents to " + f"data/pdfs/{pdf_name}")
                                f.write(response.content)
                    print("Finished!")
                break
        # if no .jl has been found that matches the given jl_file parameter:
        if not found:
            print(
                "No matching .jl file has been found. Please enter a correct file name or 'all' to download PDFs for all available .jl files."
            )


process = CrawlerProcess(settings)
process.crawl(OparlSpider, **spargs)
process.start()
download_pdfs("paper_2020-10-07T18-24-21.jl")
