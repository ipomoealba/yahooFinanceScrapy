# -*- coding: utf-8 -*-
# @Author: chenhuawei
# 不爆肝聲明：以後有問題盡量別來找我....

import scrapy
from yahooFinance.items import YahoofinanceItem


class updateSpider(scrapy.Spider):
    name = 'updateSpider'
    allow_domain = ['tw.money.yahoo.com']
    start_urls = ['https://tw.money.yahoo.com/fund/offshore']

    custom_settings = {
        'ITEM_PIPELINES': {
            'yahooFinance.pipelines.MongoDBPipeline': 1000
        }
    }

    def parse(self, response):
        companyName = response.xpath(
            '//div[@class="Ta-start Pstart-4"]/a/text()').extract()
        urls = response.xpath(
            '//div[@class="Ta-start Pstart-4"]/a/@href').extract()

        for url, cm in zip(urls, companyName):
            yield scrapy.Request(str("https://tw.money.yahoo.com" + url), callback=self.parse_fund)

    def parse_fund(self, response):
        row = response.xpath(
            '//tr[@class="Bgc-w alter-bg"]| //tr[@class="Bgc-w"]')
        cur = [u'日圓', u'英鎊', u'新台幣', u'美元', u'港幣', u'韓元', u'加拿大幣', u'新加坡幣', u'人民幣',
               u'澳幣', u'印尼盾', u'泰銖', u'馬來西亞幣', u'菲律賓披索', u'歐元', u'越南盾', u'南非幣', u'紐西蘭幣', u'瑞士法郎', u'瑞典幣']
        cure = ['JPY', 'GBP', 'NTD', 'USD', 'HKD', 'KRW', 'CAD', 'SGD', 'CNY',
                'AUD', 'IDR', 'THB', 'MYR', 'PHP', 'EUR', 'VND', 'ZAR', 'NZD', 'SFR', 'SEK']
        for r in row:
            item = YahoofinanceItem()
            item['fund_name'] = r.xpath(
                './/td[@class="Ta-start txt-left id"]/a/text()').extract()[0]
            item['id'] = r.xpath('.//td[@class="Ta-start txt-left id"]/a/@href').extract()[
                0].replace('/fund/summary/', '').replace(':FO', '')

            # item['the_latest_data_update_time'] = r.xpath('.//td[@class="Ell Ta-c date"]/text()').extract()
            # item['net_worth'] = (r.xpath('.//td[@class="Ell Ta-c closeprice"]/text()').extract()) \
            # .replace(" ","").replace( "\n", "")
            curC = r.xpath(
                './/td[@class="Ell Ta-c"]/text()').extract()[0].replace(" ", "").replace("\n", "")
            for i in range(0, len(cur)):
                # print cur[i]
                # print item['currency']
                if curC == cur[i]:
                    # print curC + " " + cure[i]
                    item['currency'] = cure[i]
                # else:
                  #  item['currency'] = "GG"
            yield item
