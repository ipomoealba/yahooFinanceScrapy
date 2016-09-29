# -*- coding: utf-8 -*-
import scrapy
from yahooFinance.db.db_helper import DB_Helper
from yahooFinance.detect.detect_manager import Detect_Manager
from yahooFinance.items import ProxyItem


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    start_urls = ["http://www.xicidaili.com/nn/"]
    # allowed_domains = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'yahooFinance.pipelines.ProxyPipeline': 300
        }
    }

    db_helper = DB_Helper()
    detecter = Detect_Manager(5)
    Page_Start = 1
    Page_End = 10
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'Referer': 'http://www.xicidaili.com/'
    }

    def parse(self, response):
        trs = response.xpath('//tr[@class="odd" or @class=""]')
        for tr in trs:
            item = ProxyItem()
            tds = tr.xpath('./td/text()').extract()
            for td in tds:
                content = td.strip()
                if len(content) > 0:
                    if content.isdigit():
                        item['port'] = content
                        print 'ip:', item['ip']
                        print 'port:', item['port']
                        break
                    if content.find('.') != -1:
                        item['ip'] = content

            yield item
        if self.Page_Start < self.Page_End:
            new_url = self.start_urls[0] + str(self.Page_Start)
            self.Page_Start += 1
            yield scrapy.Request(new_url, headers=self.headers, callback=self.parse)
