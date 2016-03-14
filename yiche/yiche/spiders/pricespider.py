# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from yiche.items import YicheItem


class PricespiderSpider(CrawlSpider):
    name = 'pricespider'
    allowed_domains = ['bitauto.com']
    start_urls = ['http://price.bitauto.com/xuanchegongju/?p=0&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'/xuanchegongju/'+r'\?p=0&page=\d*'), follow=True),
        Rule(LinkExtractor(allow=r'/nb\d*/'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = YicheItem()
        items = []
        print response.url
        sel = HtmlXPathSelector(response)
        name = sel.xpath('//h3/text()').extract()[0].strip()
        all_price = sel.xpath('//strong[@id="sDirPrice"]/text()').extract()[0].strip()
        each_name = sel.xpath('//tr/td/a/text()').extract()
        price1 = sel.xpath('//td[@style="text-align: right"]/span/text()').extract()
        price2 = sel.xpath('//td[@style="text-align: right"]/span/a/text()').extract()
        item['name'] = name
        item['all_price'] = all_price
        need1 = [each.strip() for each in each_name]
        need2 = [each.strip() for each in price1]
        need3 = [each.strip() for each in price2]
        price = zip(need1,need2,need3)
        item['price'] = price

        items.append(item)
        return items
