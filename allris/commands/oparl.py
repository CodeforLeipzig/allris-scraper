import os
from scrapy.commands import ScrapyCommand
from scrapy.utils.conf import arglist_to_dict
from scrapy.utils.python import without_none_values
from scrapy.exceptions import UsageError


class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return "[options] <city>"

    def short_desc(self):
        return "Run OparlSpider for a city"

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        # parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
        #                   help="set spider argument (may be repeated)")
        # parser.add_option("-o", "--output", metavar="FILE",
        #                   help="dump scraped items into FILE (use - for stdout)")
        # parser.add_option("-t", "--output-format", metavar="FORMAT",
        #                   help="format to use for dumping items with -o")

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)

    def run(self, args, opts):
        if len(args) < 1:
            raise UsageError()
        elif len(args) > 1:
            raise UsageError("can only run 'scrapy oparl' for a single city")

        # self.crawler_process.crawl('oparl', **opts.spargs)
        # self.crawler_process.start()
        print(opts)

        if self.crawler_process.bootstrap_failed:
            self.exitcode = 1