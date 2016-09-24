# -*- coding: utf-8 -*-
# @Author: chenhuawei

import os
import urllib
import pymongo
from yahooFinance.spiders.proxySpider import ProxySpider
from scrapy.exceptions import DropItem
from scrapy import log
from yahooFinance import settings
from scrapy.conf import settings


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db["last_data"]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item


class ProxyPipeline(object):
    proxyId = 1

    def process_item(self, item, spider):
        if spider.name == 'proxy':

            proxySpider = ProxySpider(spider)
            proxy = {'ip': item['ip'], 'port': item['port']}
            proxy_all = {'ip': item['ip'], 'port': item['port'], 'proxyId': self.proxyId}
            if proxySpider.db_helper.insert(proxy, proxy_all) == True:  # 插入数据
                self.proxyId += 1
            return item

        else:
            return item


class YahoofinancePipeline(object):
    def process_item(self, item, spider):
        # 儲存路徑
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
