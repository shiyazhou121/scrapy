# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from koubei.items import KoubeiItem


class KbspiderSpider(CrawlSpider):
    name = 'kbspider'
    allowed_domains = ['bitauto.com']
    start_urls = ['http://www.bitauto.com/']

    def parse_item(self, response):
        i = KoubeiItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
    import urllib2
    from lxml import etree
    import re
    import codecs
    import json
    import time


    def crawler(url):
        html = urllib2.urlopen(url).read()
        con = etree.HTML(html)
        return con


    #处理列表数据
    def deal1(data):
        k = []
        if len(data)==0:
            k.append('')
        elif len(data) ==1:
            k.append(data[0].strip())
        else:
            for each in data:
                k.append(each.strip())
        return k


    #处理单个数据
    def deal2(data):
        k = []
        if len(data)==0:
            k = ''
        elif len(data) ==1:
            k = data[0].strip()
        else:
            for each in data:
                k.append(each.strip())
        return k


    #得到全部车系的url
    def get_url(num):
        all_url = []
        for i in range(1,num):
            url = 'http://koubei.bitauto.com/tree/xuanche/?page=%s' %str(i)
            con = crawler(url)
            need_url = con.xpath('//div[@class="title"]/a/@href')
            all_url.extend(need_url)
        return all_url


    #得到每种车系口碑的总页数
    def get_num(url):
        html = urllib2.urlopen(url).read()
        req = re.compile(r'tags/%e7%bb%bc%e5%90%88/page(\d+)/')
        a = req.findall(html)
        b = [int(i) for i in a]
        if len(b)==0:
            return 0
        else:
            return max(b)


    #得到每种车系的全部汇总所有信息，返回成字典
    def all_need(url,point):
        index,name = get_first(url)
        other = get_second(url,point)
        index['koubei'] = other
        return index,name


    #得到每种车系第一页的汇总信息，返回成字典，包含（车名、排名、总分数、好印象、坏印象）
    def get_first(url):
        item = {}
        con = crawler(url)
        name = deal2(con.xpath('//h1/a/text()'))
        rank = deal2(con.xpath('//strong[@class="s-t"]/text()'))
        score = deal1(con.xpath('//p[@class="red_txt"]/text()'))
        good = deal1(con.xpath('//div[@class="word_box"][1]/span/a/text()'))
        bad = deal1(con.xpath('//div[@class="word_box"][2]/span/a/text()'))
        item['rank'] = rank
        item['score'] = score
        item['good'] = good
        item['bad'] = bad
        return item,name


    #得到每种车系所有页的具体口碑信息，返回该车系的口碑，列表形式
    def get_second(url,point):
        get_url = url + 'tags/%E7%BB%BC%E5%90%88/page1'#第一页的url
        num = get_num(get_url) #得到口碑总页数
        koubei = []     #初始化列表，用来保存
        for each in range(1,num+1):      #遍历这种车系的每一页
            print point,num,each
            each_url = url + 'tags/%E7%BB%BC%E5%90%88/page'+str(each)+'/'  #该页的url
            k = get_detail(each_url)        #得到该页的详细信息
            koubei.extend(k)                #合并列表，将该页信息添加到大列表
        return koubei                      #返回大列表

    #得到每页的所有用户口碑，然后添加到列表、去掉空的，返回列表，包含每页所有用户评论
    def get_detail(url):
        koubei1 = []
        con = crawler(url)
        tbody = con.xpath('//dd')
        for each in tbody:
            z = each_detail(each)
            if len(z)!=0:
                koubei1.append(z)
        return koubei1
            
    #得到每个用户的车型、各项打分、评论信息。返回字典，包含（具体车名(单项)、各项打分分数(单项)、评价内容(字典形式)）
    def each_detail(data):
        each = {}
        car = deal2(data.xpath('div/p[@class="carname"]/text()'))
        detail1 = data.xpath('div/div[@class="add_newkb_table"]/table/tbody/tr[1]/th/text()')
        detail2 = data.xpath('div/div[@class="add_newkb_table"]/table/tbody/tr[2]/td/text()')
        score = dict(zip([x.strip() for x in detail1],[x.strip() for x in detail2]))
        url = data.xpath('div/ul/li/a/@href')
        if len(url):
            comment = get_comment(url[0])
        else:
            comment = {}
        if len(car)!=0:
            each['car'] = car
            each['score'] = score
            each['comment'] = comment
            return each
        else:
            return ''

    #得到评论信息，返回字典，包含（所有链接评价内容）
    def get_comment(url):
        con = crawler(url)
        need1 = deal1(con.xpath('//div[@class="article-contents"]/p/strong/text()'))
        need2 = deal1(con.xpath('//div[@class="article-contents"]/p/text()'))
        mark = deal1(con.xpath('//div[@class="the_pages_tags"]/a/text()'))
        n = []
        for i in need2:
            if len(i)!=0:
                n.append(i)
        zidian = dict(zip(need1,n))
        zidian.setdefault('mark',mark)
        return zidian


    #保存成json文件
    def save(data,name):
        line = json.dump(data,open('yiche_koubei_'+name+'.json','a+'))

    car_url = get_url(68)
    point = 1
    print len(car_url)
    yiche_koubei = {}
    for each in car_url:
        koubei_list = []
        print '第 %s 种车系' %str(point)
        each_koubei,each_name = all_need(each,point)
        point += 1
        yiche_koubei.setdefault(each_name,each_koubei)
        koubei_list.append(each_name)
        koubei_list.append(each_koubei)
        save(koubei_list,'list')
        time.sleep(3)
    item = {}


    return i
