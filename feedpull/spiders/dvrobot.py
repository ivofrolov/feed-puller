import scrapy
from scrapy.linkextractors import LinkExtractor

from feedpull.spiders import FeedSpider


class DvrobotSpider(FeedSpider):
    name = 'dvrobot'

    feed_id = 'http://dvrobot.ru'
    feed_title = 'ДВ Робот'

    allowed_domains = ['dvrobot.ru']
    start_urls = ['http://dvrobot.ru/248/']

    link_extractors = (
        LinkExtractor(
            allow=r'/\d{3}/',
            restrict_css='.products-wrapper.products-popover-wrapper'),
    )

    selectors = {
        'title': '.product-detailed.product-page .content-wrapper h2::text',
        'content': '.products-wrapper > div:nth-child(2)',
        'img': 'img#sv-prod-thumb::attr(src)',
    }
