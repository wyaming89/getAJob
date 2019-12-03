# -*- coding: utf-8 -*-
import json
import logging
import math, copy

import scrapy
from scrapy.shell import inspect_response

from DAzhaopin.items import LagouItem



class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']

    def __init__(self):
        self.url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        self.first_url = 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90'

        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
            'Referer':
            'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90'
        }
        self.data = {'first': 'true', 'pn': '1', 'kd': '数据分析'}
        self.logging = logging.getLogger('lagouSpider')

    def start_requests(self):

        yield scrapy.Request(url=self.first_url, headers=self.header)

    def parse(self, response):
        yield scrapy.FormRequest(url=self.url,
                                 headers=self.header,
                                 callback=self.parse_content,
                                 formdata=self.data)

    def parse_content(self, response):
        content = json.loads(response.text)
        num = response.request.body.decode('utf-8').split('&')[1].split(
            '=')[-1]
        items = LagouItem()
        if content['msg'] is None:
            self.logging.info('第 %s 页返回正常' % num)
            count = content['content']['positionResult']['totalCount']
            items['res'] = content['content']['positionResult']['result']
            yield items
            i = 2
            while i <= math.ceil(count / 15):
                temp = self.data
                temp['pn'] = str(i)
                yield scrapy.FormRequest(url=self.url,
                                         headers=self.header,
                                         callback=self.parse_detail,
                                         formdata=copy.deepcopy(temp))
                i += 1
        else:
            logging.warning(content['msg'])
            return scrapy.Request(url=self.first_url,
                                  headers=self.header,
                                  priority=100,
                                  dont_filter=True)

    def parse_detail(self, response):
        content = json.loads(response.text)
        num = response.request.body.decode('utf-8').split('&')[1].split(
            '=')[-1]
        items = LagouItem()
        if content['msg'] is None:
            self.logging.info('第 %s 页返回正常' % num)
            items['res'] = content['content']['positionResult']['result']
            yield items
        else:
            self.logging.info('第 %s 页出错:%s' % (num, content['msg']))
            yield scrapy.Request(url=self.first_url,
                                 headers=self.header,
                                 priority=100,
                                 dont_filter=True)
            yield response.request.replace(dont_filter=True)

    def parse_job(self, response):
        sub = response.xpath('//dl[@class="job_detail"]')
        item = LagouItem()
        item['res'] = response.meta['item']
        item['res']['job_detail'] = sub.xpath(
            './dd/div[@class="job-detail"]//text()').re('\S+')
        item['res']['addr'] = sub.xpath(
            './dd[@class="job-address"]/div[@class="work_addr"]//text()').re(
                '\S+')
        yield item
