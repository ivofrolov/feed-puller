# Define your middlewares here
#
# Don't forget to add your spider middleware to the SPIDER_MIDDLEWARES setting
# See: https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#
# And don't forget to add your downloader middleware to the DOWNLOADER_MIDDLEWARES setting
# See: https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

import os
import time
import sqlite3

from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy.utils.request import request_fingerprint
from scrapy.utils.project import data_path
from scrapy.exceptions import NotConfigured
from scrapy import signals


class DeltaFetch(object):
    """
    This is a spider middleware to ignore requests to pages containing items
    seen in previous crawls of the same spider, thus producing a "delta crawl"
    containing only new items.
    This also speeds up the crawl, by reducing the number of requests that need
    to be crawled, and processed (typically, item requests are the most cpu
    intensive).
    It is `scrapy-deltafetch <https://github.com/scrapy-plugins/scrapy-deltafetch>`_
    library with sqlite3 support.
    """

    def __init__(self, dir, reset=False, stats=None):
        self.dir = dir
        self.reset = reset
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        s = crawler.settings
        if not s.getbool('DELTAFETCH_ENABLED'):
            raise NotConfigured
        dir = s.get('DELTAFETCH_DIR', 'deltafetch')
        reset = s.getbool('DELTAFETCH_RESET')
        o = cls(dir, reset, crawler.stats)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        dbpath = os.path.join(self.dir, '{}.db'.format(spider.name))
        self.db = sqlite3.connect(dbpath)
        self.db.execute('''CREATE TABLE IF NOT EXISTS visits
                           (page TEXT PRIMARY KEY, moment INTEGER)
                           WITHOUT ROWID''')
        if self.reset or getattr(spider, 'deltafetch_reset', False):
            self.db.execute('DELETE FROM visits')
            self.db.commit()

    def spider_closed(self, spider):
        self.db.close()

    def process_spider_output(self, response, result, spider):
        for r in result:
            if isinstance(r, Request):
                if self._page_visited(self._get_key(r)):
                    spider.logger.info('Ignoring already visited: {}'.format(r))
                    if self.stats:
                        self.stats.inc_value(
                            'deltafetch/skipped', spider=spider)
                    continue
            elif isinstance(r, (BaseItem, dict)):
                self._store_visit(self._get_key(response.request))
                if self.stats:
                    self.stats.inc_value('deltafetch/stored', spider=spider)
            yield r

    def _page_visited(self, key):
        query = 'SELECT 1 FROM visits WHERE page=?'
        cursor = self.db.execute(query, (key,))
        return (cursor.fetchone() is not None)

    def _store_visit(self, key):
        query = '''INSERT INTO visits (page, moment)
                   VALUES (?, ?)
                   ON CONFLICT (page) DO UPDATE
                   SET moment = excluded.moment'''
        self.db.execute(query, (key, time.time()))
        self.db.commit()

    def _get_key(self, request):
        key = request.meta.get('deltafetch_key')
        if not key:
            key = request_fingerprint(request)
        return key
