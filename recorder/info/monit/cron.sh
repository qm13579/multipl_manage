#! /bin/sh
export PATH=$PATH:/usr/local/bin
cd /usr/project/multipl_manage/recorder/info/monit

scrapy crawl eur --nolog  >> cron_test.log 2>&1 &

