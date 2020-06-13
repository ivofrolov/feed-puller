import scrapy
from scrapy.linkextractors import LinkExtractor

from feedpull.spiders import FeedSpider


class DiytubesSpider(FeedSpider):
    name = 'diytubes'

    feed_id = 'http://diy-tubes.ru'
    feed_title = 'diytubes'

    allowed_domains = ['diy-tubes.ru']
    start_urls = ['http://diy-tubes.ru/']

    link_extractors = (
        LinkExtractor(
            allow=r'index\.php\?route=product/product&product_id=',
            restrict_css='.box-product'),
    )

    selectors = {
        'title': '#content > h1::text',
        'content': '#tab-description',
        'img': '#image::attr(src)',
    }
