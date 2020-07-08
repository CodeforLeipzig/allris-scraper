from pathlib import Path
from tika import parser
import os


def extract_text_from_pdfs_recursively():
    for root, dirs, files in os.walk("data/pdfs"):
        for file in files:
            path_to_pdf = os.path.join(root, file)
            [stem, ext] = os.path.splitext(path_to_pdf)
            file_name = stem.split("/")[-1]
            if ext == ".pdf":
                print("Processing " + path_to_pdf)
                pdf_contents = parser.from_file(path_to_pdf)
                Path("data/txts").mkdir(parents=True, exist_ok=True)
                path_to_txt = "data/txts/" + file_name + ".txt"
                txt_path = Path(path_to_txt)
                if not txt_path.is_file():
                    with open(path_to_txt, "w") as txt_file:
                        print("Writing contents to " + path_to_txt)
                        text = pdf_contents["content"]
                        txt_file.write(
                            os.linesep.join([s for s in text.splitlines() if s])
                        )  # removes empty lines; some lines with just a single white space character still remain, but might be useful for later segmentation?
    print("finished!")


extract_text_from_pdfs_recursively()
