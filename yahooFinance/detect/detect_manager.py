# -*- coding: utf-8 -*-
# @Author: ipomoealba
from threading import Thread
import time

from yahooFinance.db.db_helper import DB_Helper
from yahooFinance.detect.detect_proxy import Detect_Proxy

'''
define a thread manager
'''


class Detect_Manager(Thread):
    def __init__(self, threadSum):
        Thread.__init__(self)
        sqldb = DB_Helper()
        sqldb.updateID()
        self.pool = []
        for i in range(threadSum):
            self.pool.append(Detect_Proxy(DB_Helper(), i + 1, threadSum))

    def run(self):
        self.startManager()
        self.checkState()

    def startManager(self):
        for thread in self.pool:
            thread.start()

    def checkState(self):
        now = 0
        while now < len(self.pool):
            for thread in self.pool:
                if thread.isAlive():
                    now = 0
                    break
                else:
                    now += 1
            time.sleep(0.1)
        goodNum = 0
        badNum = 0
        for i in self.pool:
            goodNum += i.goodNum
            badNum += i.badNum
        sqldb = DB_Helper()
        sqldb.updateID()
        print 'proxy good Num ---', goodNum
        print 'proxy bad Num ---', badNum
