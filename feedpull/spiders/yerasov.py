import scrapy
from scrapy.linkextractors import LinkExtractor

from feedpull.spiders import FeedSpider


class YerasovSpider(FeedSpider):
    name = 'yerasov'

    feed_id = 'https://www.yerasov.ru'
    feed_title = 'yerasov'

    allowed_domains = ['www.yerasov.ru']
    start_urls = ['https://www.yerasov.ru/catalog/umelye-ruki']

    link_extractors = (
        LinkExtractor(
            allow=r'/catalog/',
            restrict_css='#views-bootstrap-grid-1'),
    )

    selectors = {
        'title': 'h1.page-header > span::text',
        'content': '#block-system-main',
        'img': '.field-name-uc-product-image img::attr(src)',
    }
