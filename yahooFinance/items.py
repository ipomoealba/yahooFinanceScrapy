# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# -*- coding: utf-8 -*-
# @Author: chenhuawei

import scrapy


class YahoofinanceItem(scrapy.Item):

    fund_name = scrapy.Field()
    the_latest_data_update_time = scrapy.Field()
    net_worth = scrapy.Field()
    currency = scrapy.Field()
    
    # History data from yahoo.
    # raw type: csv
    fund_history = scrapy.Field()
    company_name = scrapy.Field()

