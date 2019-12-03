import random, time, logging, json
from urllib.parse import quote

import requests
import redis

searchWord = [
    '数据分析',
    '数据挖掘',
    '人工智能',
    '机器学习',
    '深度学习',
]
searchWord = [quote(s) for s in searchWord]
url = 'https://www.lagou.com/jobs/list_%s'
ua = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'
]
logger = logging.getLogger('getcookie')
logger.setLevel(logging.INFO)

redis = redis.Redis('localhost', 6381)


def _prourl():
    item = {}
    item['url'] = url % random.choice(searchWord)
    item['headers'] = {'user-agent': random.choice(ua)}
    return item

def getcookie():

    for _ in range(5):
        item = _prourl()
        time.sleep(5)
        logger.info('start get cookie from lagou')
        cookies = requests.get(
            url=item['url'],
            headers=item['headers']
        ).cookies
        cookie = requests.utils.dict_from_cookiejar(cookies)
        res = {}
        res['headers'] = item['headers']
        res['cookie'] = cookie
        res['headers']['Referer'] = item['url']
        logger.info('the cookie is %s'%cookie)
        redis.sadd('header:cookie', json.dumps(res))
        print('update data to redis')


if __name__ == "__main__":
    getcookie()