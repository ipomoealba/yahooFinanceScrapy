# -*- coding: utf-8 -*-
# @Author: chenhuawei

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
        companyName = response.xpath('//div[@class="Ta-start Pstart-4"]/a/text()').extract()
        urls = response.xpath('//div[@class="Ta-start Pstart-4"]/a/@href').extract()

        for url, cm in zip(urls, companyName):
            yield scrapy.Request(str("https://tw.money.yahoo.com" + url), callback=self.parse_fund)

    def parse_fund(self, response):
        row = response.xpath('//tr[@class="Bgc-w alter-bg"]| //tr[@class="Bgc-w"]')

        for r in row:
            item = YahoofinanceItem()
            print(r.xpath('.//td[@class="Ta-start txt-left id"]/a/text()').extract())
            item['fund_name'] = r.xpath('.//td[@class="Ta-start txt-left id"]/a/text()').extract()
            item['the_latest_data_update_time'] = r.xpath('.//td[@class="Ell Ta-c date"]/text()').extract()
            item['net_worth'] = (r.xpath('.//td[@class="Ell Ta-c closeprice"]/text()').extract()) \
                # .replace(" ","").replace( "\n", "")
            item['currency'] = r.xpath('.//td[@class="Ell Ta-c"]/text()').extract() \
                # .replace(" ", "").replace("\n", "")
            yield item

            # test code
            # r = row[0]
            # item = YahoofinanceItem()
            # item['fund_name'] = str(r.xpath('.//td[@class="Ta-start txt-left id"]/a/text()').extract())
            # item['the_latest_data_update_time'] = str(r.xpath('.//td[@class="Ell Ta-c date"]/text()').extract()).replace(
            #     " ", "").replace("\n", "")
            # item['net_worth'] = str(r.xpath('.//td[@class="Ell Ta-c closeprice"]/text()').extract()).replace(" ","").replace("\n","")
            # item['currency'] = str(r.xpath('.//td[@class="Ell Ta-c"]/text()').extract()).replace(" ","").replace("\n","")
            # return item
