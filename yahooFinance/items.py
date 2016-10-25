# -*- coding: utf-8 -*-
# @Author: chenhuawei

import scrapy


class YahoofinanceItem(scrapy.Item):
    fund_name = scrapy.Field()
    the_latest_data_update_time = scrapy.Field()
    net_worth = scrapy.Field()
    currency = scrapy.Field()
    company_name = scrapy.Field()
    id = scrapy.Field()

class HistoryItem(scrapy.Item):
    # chinese_name = scrapy.Field()
    # currency = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    net_worth = scrapy.Field()
    up_and_down = scrapy.Field()
    the_percent_up_and_down = scrapy.Field()


class ProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
