# Define your item exporters here
#
# Don't forget to add your exporter to the FEED_EXPORTERS setting
# See: https://docs.scrapy.org/en/latest/topics/exporters.html

from scrapy.exporters import BaseItemExporter
from feedgen.feed import FeedGenerator


class AtomItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        feed_id = kwargs.pop('feed_id', 'https://scrapy.org')
        feed_title = kwargs.pop('feed_title', 'Scrapy')
        
        kwargs.update(
            fields_to_export=('title', 'url', 'img', 'content'))
        super().__init__(**kwargs)
        if not self.encoding:
            self.encoding = 'utf-8'
        
        self.file = file
        self.fg = FeedGenerator()
        self.fg.id(feed_id)
        self.fg.title(feed_title)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        if hasattr(crawler.spider, 'feed_id'):
            kwargs.update(feed_id=crawler.spider.feed_id)
        if hasattr(crawler.spider, 'feed_title'):
            kwargs.update(feed_title=crawler.spider.feed_title)

        return cls(*args, **kwargs)

    def finish_exporting(self):
        self.fg.atom_file(self.file, pretty=True, encoding=self.encoding)

    def export_item(self, item):
        fields = dict(self._get_serialized_fields(item, default_value='', include_empty=True))
        fe = self.fg.add_entry()
        fe.title(fields['title'])
        fe.id(fields['url'])
        fe.link({'href': fields['url']})
        content = fields['content']
        if fields['img']:
            content = '<img src="{}" />'.format(fields['img']) + content
        if content:
            fe.content(content=content)
        else:
            fe.content(src=fields['url'])
