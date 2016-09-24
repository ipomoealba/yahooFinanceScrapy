# -*- coding: utf-8 -*-
# @Author: ipomoealba
from pymongo import MongoClient
from scrapy.conf import settings

class DB_Helper(object):
    def __init__(self):
        client = MongoClient(settings['MONGODB_HOST'], settings['MONGODB_PORT'])
        self.db = client[settings['MONGODB_DB']]
        # client = MongoClient()
        # db = client.proxy
        self.proxys = self.db["proxylist"]

    def insert(self, condition, value):

        if self.find(condition) == False:
            self.proxys.insert(value)
            return True
        else:
            return False

    def find(self, condition):
        result = self.proxys.find_one(condition)
        if result != None:
            return True
        else:
            return False

    def delete(self, condition):
        self.proxys.remove(condition)

    def updateID(self):
        proxys = self.proxys.find()
        proxyId = 1
        for proxy in proxys:
            ip = proxy['ip']
            port = proxy['port']
            self.proxys.update({'ip': ip, 'port': port}, {'$set': {'proxyId': proxyId}})
            proxyId += 1
