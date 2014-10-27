# -*- coding: utf-8 -*-

# Scrapy settings for allris project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Allris scraper'

SPIDER_MODULES = ['allris.spiders']
NEWSPIDER_MODULE = 'allris.spiders'
USER_AGENT = 'Allris Scraper - OK Lab Leipzig (+http://codefor.de/leipzig/)'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'allris (+http://www.yourdomain.com)'
