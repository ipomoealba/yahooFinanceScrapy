# -*- coding: utf-8 -*-
# @Author: chenhuawei

import csv
import scrapy
from yahooFinance.items import HistoryItem
from pymongo import MongoClient

url_download_head = "https://tw.money.yahoo.com/fund/download/"
url_download_tail = "?startDate=1900-01-01&endDate=2016-09-19"


class financeSpider(scrapy.Spider):
    name = 'history'
    allow_domain = ['tw.money.yahoo.com']
    start_urls = ['https://tw.money.yahoo.com/fund/offshore']
    custom_settings = {
        'ITEM_PIPELINES': {
            'yahooFinance.pipelines.YahoofinancePipeline': 300
        }
    }

    def parse(self, response):
        companyName = response.xpath('//div[@class="Ta-start Pstart-4"]/a/text()').extract()
        urls = response.xpath('//div[@class="Ta-start Pstart-4"]/a/@href').extract()

        for url, cm in zip(urls, companyName):
            # zhprint(cm)
            yield scrapy.Request(str("https://tw.money.yahoo.com" + url), callback=self.parse_fund)

    def parse_fund(self, response):
        print("[!] Loading...")
        row = response.xpath('//tr[@class="Bgc-w alter-bg"]| //tr[@class="Bgc-w"]')
        for r in row:
            # item = HistoryItem()
            # item["file_urls"] = [str("https://tw.money.yahoo.com/fund/download/" + url.split('/')[3].split("'")[
            #     0] + '?startDate=1900-01-01&endDate=2016-09-19')]
            yield scrapy.Request(str(url_download_head +
                                     str(r.xpath('.//td[@class="Ta-start txt-left id"]/a/@href').extract()).split('/')[
                                         3].split("'")[
                                         0] + url_download_tail), callback=self.parse_history)

    def parse_history(self, response):
        raw_data = response.body.split()[1:]
        for i in raw_data:
            print(i.split(',')[0])
            item = HistoryItem()
            item['name'] = response.url.replace(url_download_head, '').replace(url_download_tail, '').replace(':FO', '')
            item['date'] = i.split(',')[0]
            item['net_worth'] = i.split(',')[1]
            item['up_and_down'] = i.split(',')[2]
            item['the_percent_up_and_down'] = i.split(',')[3]
            yield item
