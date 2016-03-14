# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from douban.items import DoubanItem


class Spider2Spider(CrawlSpider):
    name = 'spider2'
    allowed_domains = ['music.douban.com']
    start_urls = ['http://music.douban.com/subject_search?start=0&search_text=%E5%91%A8%E6%9D%B0%E4%BC%A6']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/subject_search\?start=\d*&search_text=%E5%91%A8%E6%9D%B0%E4%BC%A6'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = DoubanItem()
        items = []
        sel = HtmlXPathSelector(response)
        item['link'] = response.url
        item['name'] = sel.xpath('//tr[@class="item"]/td/a/@title').extract()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        items.append(item)
        return items
