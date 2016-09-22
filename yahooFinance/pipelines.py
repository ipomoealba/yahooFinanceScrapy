# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib

from yahooFinance import settings


class YahoofinancePipeline(object):
    def process_item(self, item, spider):
        # # 儲存路徑
        # dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)
        # print('dir_path', dir_path)
        #
        # if not os.path.exists(dir_path):
        #     os.makedirs(dir_path)
        #
        # # 以下預備儲存歷史資料
        # for h in item[fund_history]:
        #     pass
        return item
