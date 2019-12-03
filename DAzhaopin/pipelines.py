# -*- coding: utf-8 -*-

import logging
from DAzhaopin.items import BossItem, LagouItem, JobdescItem

from pymongo import MongoClient


class DazhaopinPipeline(object):



    def process_item(self, item, spider):
        client = MongoClient('localhost', 32768)
        db = client['zhaopin']
        if isinstance(item, BossItem):
            if item['title'].find('数据分析') != -1:
                db['boss'].insert_many([item])
                return item
            else:
                return
        elif isinstance(item, LagouItem):
            db['lagou'].insert_many(item['res'])
            return item
        elif isinstance(item, JobdescItem):
            posid = item['positionId']
            db['jobs'].insert_many([dict(item)])
            client.close()
            return item
