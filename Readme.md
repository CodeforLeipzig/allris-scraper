# Allris-Scraper

A scraper for [ratsinfo.leipzig.de](https://ratsinfo.leipzig.de/).

## Requirements

### Runtime

- [docker](https://docs.docker.com/get-docker/)

### Development

- [Python 3.8](https://www.python.org/downloads/)
- [pyenv](https://github.com/pyenv/pyenv) (optional)

## Usage

### Using docker

Build the docker image

```
docker build -t codeforleipzig/allris-scraper:latest .
```

Run the docker container

```
docker run -v $(pwd)/data:/app/data --rm codeforleipzig/allris-scraper
```

### Using python

It is recommended to use a [virtual environment](https://docs.python.org/3/tutorial/venv.html) in order to isolate libraries used in this project from the environment of your operating system. To do so, run the following in the project directory:

```
# create the virtual environment in the project directory; do this once
python -m venv venv

# activate the environment; do this before working with the scraper
source venv/bin/activate

# install the required libraries
pip install -r requirements.txt
```

To run the scraper using python:

```
python ./leipzig.py
```

### Scraper Output

The scraper writes its output to the `data` directory. One file per scraping session is written, the convention for the filename is `<OParl object type>_<current timestamp>.jl`. For example, when scraping papers: `paper_2020-06-19T10-19-16.jl`.

The output is a feed in [JSONLines](http://jsonlines.org/) format, which means one scraped JSON document per line. For inspecting the data, the [jq](https://stedolan.github.io/jq/) is useful and can be used line this:

```
# all documents in the file
cat path/to/file | jq .

# only the first document
head -n1 path/to/file | jq .
```

### Extraction of PDF and TXT files

The method download_pdfs() in the leipzig.py file downloads all PDFs, linked in the the [JSONLines](http://jsonlines.org/) files and saves them in `data/pdfs`. Files that are already saved in the folder will not be downloaded.

From the PDF files, TXT files can be generated with the extract_text_from_pdfs_recursively() method in txt_extraction.py, using [Tika](https://tika.apache.org/). The TXTs will be saved to `data/txts`. Files that are already saved in the folder will not be extracted.

### Configuration

Scrapy allows for configuration on various levels. General configuration can be found in `allris/settings.py`. For the purposes of this project, relevant values are overridden in `leipzig.py`. Per default, it is configured towards development needs. Specifically, aggressive caching is enabled (`HTTP_CACHE_ENABLED`) and the number of scraped pages is limited (`CLOSESPIDER_PAGECOUNT`).

### NLP

#### Data Preparation

nlp.py provides a method read_txts_into_dataframe() to read all TXT files in `data/txts` into a pandas dataframe and a method write_df_to_csv() to save this dataframe in csv format as `data.csv` in the `data` folder.

#### Topic Modeling

To make the obtained documents more accessible for users interested in certain topics, a topic modeling has been run on the extracted documents with the R software [tidyToPān](https://zenodo.org/badge/latestdoi/233335696). The obtained model will be used later on for e.g. a search function.
