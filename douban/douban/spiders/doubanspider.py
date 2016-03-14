# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from douban.items import DoubanItem
from scrapy.selector import Selector
from scrapy.http import Request

class DoubanspiderSpider(Spider):
    name = 'spider'
    download_delay = 1
    allowed_domains = ['douban.com']
    start_urls = ['http://movie.douban.com/subject_search?start=0&search_text=%E5%91%A8%E6%9D%B0%E4%BC%A6&cat=1002']


    def parse(self, response):
        item = DoubanItem()
        sel = Selector(response)
        items = []
        name = sel.xpath('//tr[@class="item"]/td/a/@title').extract()
        link = sel.xpath('//span[@class="next"]/a/@href').extract()
        item['name'] = [t.encode('utf-8').strip() for t in name]
        item['link'] = str(response.url).encode('utf-8')
        items.append(item)
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        yield item
        for url in link:
            print url
            yield Request(url,callback = self.parse)

