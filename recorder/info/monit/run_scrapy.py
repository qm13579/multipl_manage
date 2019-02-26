#!/usr/bin/python
from scrapy import cmdline

if __name__ == '__main__':
    #methods 1
    cmdline.execute('scrapy crawl eur --nolog'.split())
