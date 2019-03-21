# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from publicsentiment.models import WenInfo
from scrapy_djangoitem import DjangoItem

class SentimentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class WebinfoItem(DjangoItem):

    django_model = WenInfo


