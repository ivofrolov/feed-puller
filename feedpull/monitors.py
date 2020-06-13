from spidermon import MonitorSuite
from spidermon.contrib.scrapy.monitors import (FinishReasonMonitor,
                                               ErrorCountMonitor,
                                               UnwantedHTTPCodesMonitor)
from spidermon.contrib.actions.telegram.notifiers import SendTelegramMessageSpiderFinished


class SpiderCloseMonitorSuite(MonitorSuite):
    monitors = [
        FinishReasonMonitor,
        ErrorCountMonitor,
        UnwantedHTTPCodesMonitor,
    ]

    monitors_failed_actions = [
        SendTelegramMessageSpiderFinished,
    ]
