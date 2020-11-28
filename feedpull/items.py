# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
import readability


def make_readable(content):
    return readability.Document(content).summary(html_partial=True)


class FeedItem(Item):
    title = Field()
    content = Field()
    url = Field()
    img = Field()


class FeedItemLoader(ItemLoader):
    default_item_class = FeedItem
    default_output_processor = TakeFirst()

    title_in = MapCompose(str.strip)
    content_in = MapCompose(make_readable)
