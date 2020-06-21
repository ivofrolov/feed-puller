import logging
import re


def remove_uri_credentials(record: logging.LogRecord):
    record.args['uri'] = re.sub(
        r'(\w+:\/\/)(.+:.+@)(.+)',
        r'\g<1>\g<3>',
        record.args['uri'])
    return True


logging.getLogger('scrapy.extensions.feedexport').addFilter(remove_uri_credentials)
