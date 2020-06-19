# Allris-Scraper

A scraper for [ratsinfo.leipzig.de](https://ratsinfo.leipzig.de/).

## Requirements

### Runtime

* [docker](https://docs.docker.com/get-docker/)

### Development
* Python 3.6.9
* pip 9.0.1
* virtualenv (optional) (https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv)
* virtualenvwrapper (optional)

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

Ensure that all development dependencies are installed, then run:
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

### Configuration

Scrapy allows for configuration on various levels. General configuration can be found in `allris/settings.py`. For the purposes of this project, relevant values are overridden in `leipzig.py`. Per default, it is configured towards development needs. Specifically, aggressive caching is enabled (`HTTP_CACHE_ENABLED`) and the number of scraped pages is limited (`CLOSESPIDER_PAGECOUNT`).