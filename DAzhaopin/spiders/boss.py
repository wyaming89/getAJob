# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy_splash import SplashRequest


class BossSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['zhipin.com']

    #start_urls = ['http://zhipin.com/']

    def __init__(self):
        self.url = 'https://www.zhipin.com/c101280100/?query=%s&page=%s'

    def start_requests(self):
        param = ('数据分析', '1')
        yield SplashRequest(self.url % param,
                            self.parse_city,
                            args={
                                'wait': 2,
                                'image': 0
                            },
                            endpoint='render.html')

    def parse_city(self, response):
        sub = response.xpath(
            '//dd[@class="city-wrapper"]/a[@ka]/@href').extract()
        for s in sub:
            url = 'https://www.zhipin.com%s' % s
            yield SplashRequest(url=url,
                                callback=self.parse,
                                endpoint='render.html',
                                args={
                                    'wait': 1.5,
                                    'image': 0,
                                    'headers': {
                                        'Referer': ''
                                    }
                                })

    def parse(self, response):
        sub = response.xpath(
            '//div[@class="job-list"]/ul/li/div[@class="job-primary"]')
        url = 'https://www.zhipin.com%s'
        for s in sub:
            item = {}
            position = s.xpath('./div[@class="info-primary"]')
            item['title'] = position.xpath(
                '//div[@class="job-title"]/text()').extract_first()
            item['detail_url'] = position.xpath('./h3/a/@href').extract_first()
            item['salary'] = position.xpath(
                './h3/a/span/text()').extract_first()
            item['city'], *item['workyear'], item['edution'] = tuple(
                position.xpath('./p//text()').extract())

            company = s.xpath('./div[@class="info-company"]')
            item['company'] = company.xpath('./div/h3/a/@href').extract_first()
            item['companyName'] = company.xpath(
                './div/h3/a/text()').extract_first()
            item['companyfield'], *item['financestage'], item[
                'companysize'] = tuple(
                    company.xpath('./div/p//text()').extract())

            yield SplashRequest(
                url=url % item['detail_url'],
                callback=self.parse_detail,
                meta=item,
                endpoint='render.html',
                args={
                    'wait':1.5,
                    'image':0,
                    'headers':{
                        'Referer':''
                    }
                }
            )
        next_page = response.xpath(
            '//div[@class="page"]/a[@class="next"]/@href').extract_first()
        if next_page != 'javascript:;':

            yield SplashRequest(url=url % next_page,
                                callback=self.parse,
                                endpoint='render.html',
                                args={
                                    'wait': 1.5,
                                    'image': 0,
                                    'headers': {
                                        'Referer': ''
                                    }
                                })
        else:
            return

    def parse_detail(self, response):
        sub = response.xpath('//div[@class="detail-content"]')
        item = response.meta
        item['job_description'] = sub.xpath(
            './div[@class="job-sec"][1]/div//text()').extract()
        item['addr'] = sub.xpath(
            '//div[@class="job-location"]/div/text()').extract()
        yield item
