import json
from w3lib.http import basic_auth_header
from scrapy.spiders import CrawlSpider, Rule

from feedpull.items import FeedItemLoader


class FeedSpider(CrawlSpider):
    feed_id = None
    feed_title = None
    link_extractors = ()
    selectors = {}

    def __init__(self, *args, **kwargs):
        self.rules = [Rule(ext, callback='parse_item') for ext in self.link_extractors]
        super().__init__(*args, **kwargs)

    def parse_item(self, response):
        item = FeedItemLoader(response=response)
        for field, selector in self.selectors.items():
            item.add_css(field, selector)
        item.add_value('url', response.url)
        return item.load_item()
