from pathlib import Path
import json
import requests as re

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
                    print("Processing " + f"data/pdfs/{pdf_name}")
                    if not pdf_name.startswith("1047735.pdf"):
                        pdf_url = paper_json["mainFile"]["accessUrl"]
                        response = re.get(pdf_url)
                        Path("data/pdfs").mkdir(parents=True, exist_ok=True)
                        with open(f"data/pdfs/{pdf_name}", "wb") as f:
                            print("Writing contents to " + f"data/pdfs/{pdf_name}")
                            f.write(response.content)
    print("finished!")


download_pdfs()
