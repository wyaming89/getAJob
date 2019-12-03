# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from DAzhaopin.items import JobdescItem
import logging


class JobdescSpider(scrapy.Spider):
    name = 'jobdesc'
    allowed_domains = ['lagou.com']
    db = MongoClient('mongodb://localhost:32768')['zhaopin']
    logging = logging.getLogger(__name__)

    def start_requests(self):
        idset = set([p['positionId'] for p in self.db['jobs'].find({})])
        pidset = set([p['positionId'] for p in self.db['lagou'].find({})])
        posid = pidset.difference(idset)
        
        url = 'https://www.lagou.com/jobs/%s.html'
        count = len(posid)
        for n, value in enumerate(posid):
            yield scrapy.Request(url % value, meta={'positionId': value, 'count':(n+1, count)})

    def parse(self, response):
        self.logging.info('正在处理%s'%response.url)

        sub = response.xpath('//dl[@class="job_detail"]')
        item = JobdescItem()
        job_detail = sub.xpath('./dd/div[@class="job-detail"]//text()').re('\S+')
        job_addr = sub.xpath('//div[@class="work_addr"]//text()').re('\S+')[:-1]
        if job_addr and job_detail:
            self.logging.info('处理进度%d / %d' % response.meta['count'])
            item['positionId'] = response.meta['positionId']
            item['job_detail'] = job_detail
            item['job_addr'] = job_addr
            yield item
        else:
            self.logging.info('重新处理%s'%response.meta['positionId'])
            yield scrapy.Request('https://www.lagou.com/jobs/%s.html'%response.meta['positionId'], dont_filter=True, meta=response.meta)
