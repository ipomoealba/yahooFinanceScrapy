# -*- coding: utf-8 -*-
# @Author: chenhuawei

import scrapy


class financeSpider(scrapy.Spider):
    name = 'history'
    allow_domain = ['tw.money.yahoo.com']
    start_urls = ['https://tw.money.yahoo.com/fund/offshore']

    def parse(self, response):
        companyName = response.xpath('//div[@class="Ta-start Pstart-4"]/a/text()').extract()
        urls = response.xpath('//div[@class="Ta-start Pstart-4"]/a/@href').extract()

        for url, cm in zip(urls, companyName):
            # zhprint(cm)
            yield scrapy.Request(str("https://tw.money.yahoo.com" + url), callback=self.parse_fund)

    def parse_fund(self, response):
        print("[!] Loading...")
        row = response.xpath('//tr[@class="Bgc-w alter-bg"]| tr[@class="Bgc-w"]')
        for r in row:
            url = str(r.xpath('.//td[@class="Ta-start txt-left id"]/a/@href').extract())
            # print(str("https://tw.money.yahoo.com/fund/download/" + url.split('/')[3].split("'")[
            #     0] + '?startDate=1900-01-01&endDate=2016-09-19'))
            yield scrapy.Request(str("https://tw.money.yahoo.com/fund/download/" + url.split('/')[3].split("'")[
                0] + '?startDate=1900-01-01&endDate=2016-09-19'), callback=self.parse_history)

    def parse_history(self, response):
        print ("[!] Saving data....")
        path = self.get_path(response.url)
        with open(path, "wb") as f:
            f.write(response.body)
