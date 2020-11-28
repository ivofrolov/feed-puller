from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor

from feedpull.spiders import FeedSpider


class SchneidersladenSpider(FeedSpider):
    name = 'schneidersladen'

    feed_id = 'http://schneidersladen.de'
    feed_title = 'schneidersladen'

    allowed_domains = ['schneidersladen.de']
    start_urls = ['http://schneidersladen.de/en/new-stuff/']

    link_extractors = (
        LinkExtractor(restrict_css='.listing'),
    )

    selectors = {
        'title': '.product--title::text',
        'content': '.product--description',
        'img': '.image--media>img::attr(src)',
    }

    def parse_start_url(self, response, **kwargs):
        last_page_selector = '.listing--paging .paging--display'
        last_page = response.css(last_page_selector).re_first(r'\d')
        for page in range(1, int(last_page) + 1):
            yield response.follow(f'?p={page}')
