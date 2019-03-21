# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re
from publicsentiment import models
import hashlib
from ..items import WebinfoItem
import time

url_dict={
    'people':'http://www.people.com.cn',
          }

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['http://www.people.com.cn/']
    start_urls = ['http://www.people.com.cn//']
    current = time.strftime('%Y-%m-%d', time.localtime())

    def parse(self, response):
        fun_key=match_url(response.url)
        obj=getattr(NewsSpider,fun_key)
        res = obj(self,response)
        for i in res:
            item_obj = WebinfoItem(
                title=i['title'],
                url=i['url'],
                url_md5=i['url_md5'],
                url_info=i['url_info'],
            )
            yield item_obj
    def people(self,response):
        '''处理people相关信息'''
        #通过urlinfo数据库获取相关历史标题
        obj = models.UrlInfo.objects.get(url=response.url)
        web_info = obj.weninfo_set.all()
        print('--开始解析')
        info = info_set(web_info)
        #解析处理
        print('开始解析')
        con_list = []
        for tag_a in Selector(response=response).xpath('//ul[@class="list14"]'):
            url = tag_a.xpath('.//li//a//@href').extract()
            title = tag_a.xpath('.//li//a//text()').extract()
            for u,t in zip(url,title):
                md5_url = md5(u)
                if md5_url in info:continue # 判断当前url是否已存在
                info.add(md5_url)
                con_list.append(
                    {'title':t,'url':u,'url_md5':md5_url,'url_info':obj}
                )
        return con_list




def match_url(url):
    for k,v in url_dict.items():
        response=re.findall('.*%s.*'%v,url)
        if response:
            return k
        else:
            return False
def md5(url):
    'url to md5'
    obj = hashlib.md5()
    obj.update(bytes(url,encoding='utf-8'))
    return obj.hexdigest()
def info_set(data):
    '集合去重'
    info=set()
    for con in data:
        info.add(con.url_md5)
    return info