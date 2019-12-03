# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BossItem(scrapy.Item):
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
    item = scrapy.Field()


class LagouItem(scrapy.Item):
    res = scrapy.Field()

class JobdescItem(scrapy.Item):
    positionId = scrapy.Field()
    job_detail = scrapy.Field()
    job_addr = scrapy.Field()
