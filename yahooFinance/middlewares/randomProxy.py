# -*- coding: utf-8 -*-
# @Author: ipomoealba
# coding:utf-8

import random

from yahooFinance import settings

from yahooFinance.db.db_helper import DB_Helper

'''

random Proxy

'''


class RandomProxy(object):
    def __init__(self):

        self.db_helper = DB_Helper()

        self.count = self.db_helper.proxys.count()

    def process_request(self, request, spider):
        '''

        :param request:

        :param spider:

        :return:

        '''

        request.meta['proxy'] = settings.HTTP_PROXY
