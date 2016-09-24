# -*- coding: utf-8 -*-
# @Author: ipomoealba
import socket
from threading import Thread

import urllib

'''
detect proxy can be used or not
'''


class Detect_Proxy(Thread):
    url = 'http://ip.chinaz.com/getip.aspx'

    def __init__(self, db_helper, part, sum):
        Thread.__init__(self)
        self.db_helper = db_helper
        self.part = part
        self.sum = sum
        self.counts = self.db_helper.proxys.count()
        socket.setdefaulttimeout(2)
        self.__goodNum = 0
        self.__badNum = 0

    @property
    def goodNum(self):
        return self.__goodNum

    @goodNum.setter
    def goodNum(self, value):
        self.__goodNum = value

    @property
    def badNum(self):
        return self.__badNum

    @badNum.setter
    def badNum(self, value):
        self.__badNum = value

    def run(self):

        self.detect()  # 开始检测

    def detect(self):

        if self.counts < self.sum:
            return

        pre = self.counts / self.sum
        start = pre * (self.part - 1)
        end = pre * self.part
        if self.part == self.sum:
            end = self.counts
        proxys = self.db_helper.proxys.find({'proxyId': {'$gt': start, '$lte': end}})

        for proxy in proxys:

            ip = proxy['ip']
            port = proxy['port']
            try:
                proxy_host = "http://ha:ha@" + ip + ':' + port
                response = urllib.urlopen(self.url, proxies={"http": proxy_host})
                if response.getcode() != 200:
                    self.db_helper.delete({'ip': ip, 'port': port})
                    self.__badNum += 1
                    print proxy_host, 'bad proxy'
                else:
                    self.__goodNum += 1
                    print proxy_host, 'success proxy'

            except Exception, e:
                print proxy_host, 'bad proxy'
                self.db_helper.delete({'ip': ip, 'port': port})
                self.__badNum += 1
                continue
