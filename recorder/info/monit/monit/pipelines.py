# -*- coding: utf-8 -*-
import sys
# from ... import models
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MonitPipeline(object):
    def process_item(self, item, spider):
        return item

class EuropaPipline(object):
    task_lists=[]
    def process_item(self,item,spider):
        print(item['title'],item['href'],item['md5'])

        self.task_lists.append(models.WebInfo(
            title=item['title'],
            url=item['href'],
            md5=item['md5']))
        print('lenlist:',len(self.task_lists))
        models.WebInfo.objects.bulk_create(self.task_lists)