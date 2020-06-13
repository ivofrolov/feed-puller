import scrapy
from scrapy.linkextractors import LinkExtractor

from feedpull.spiders import FeedSpider


class AmperkaSpider(FeedSpider):
    name = 'amperka'

    feed_id = 'http://amperka.ru'
    feed_title = 'Амперка'

    allowed_domains = ['amperka.ru']
    start_urls = ['https://amperka.ru/collection/new']

    link_extractors = (
        LinkExtractor(allow=r'/product/', restrict_css='.products'),
    )

    selectors = {
        'title': '.product-detail__title::text',
        'content': '.product-detail__description',
        'img': '.gallery__images img.gallery__image::attr(src)',
    }
