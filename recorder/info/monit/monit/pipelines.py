# -*- coding: utf-8 -*-
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
        # pass
        # print(item['title'],item['md5'])
        item.save()