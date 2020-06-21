import scrapy
from scrapy.linkextractors import LinkExtractor

from feedpull.spiders import FeedSpider


class ThonkSpider(FeedSpider):
    name = 'thonk'

    feed_id = 'https://thonk.co.uk'
    feed_title = 'Thonk'

    allowed_domains = ['thonk.co.uk']
    start_urls = ['https://thonk.co.uk']

    link_extractors = (
        LinkExtractor(allow=r'/shop/', restrict_css='.products'),
    )

    selectors = {
        'title': '.product_title::text',
        'content': '#tab-description',
        'img': '.woocommerce-product-gallery__image>a::attr(href)',
    }
