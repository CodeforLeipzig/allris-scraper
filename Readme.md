# Allris-Scraper

Scrapping data from [ratsinfo.leipzig.de](https://ratsinfo.leipzig.de/)

## Requirements

* Python 3.6.9
* pip 9.0.1
* virtualenv (optional) (https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv)
* virtualenvwrapper (optional)


## Installation and scrape

* Make a new virtualenv and switch to it. (optional)
** virtualenv ~/virtualenvironment/allris
** cd ~/virtualenvironment/allris
** source activate
* cd your/checked-out/allris-scraper
* Install requirements with:
```
python3 -m pip install -r requirements.txt
```

* Run with
```
python3 leipzig.py
```

## Thoughts

* implement caching or db
* update data from last scrape date

## Todo
* field originator needs to be validated
