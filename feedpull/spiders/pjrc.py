import scrapy
from scrapy.linkextractors import LinkExtractor

from feedpull.spiders import FeedSpider


class PjrcSpider(FeedSpider):
    name = 'pjrc'

    feed_id = 'https://pjrc.com'
    feed_title = 'PJRC: Electronic Projects'

    allowed_domains = ['pjrc.com', 'www.pjrc.com']
    start_urls = ['https://www.pjrc.com/']

    link_extractors = (
        LinkExtractor(deny=[r'/forum', r'/blog/$'], restrict_css='#primary'),
    )

    selectors = {
        'title': '.entry-title a::text',
        'content': '.entry-content',
    }
