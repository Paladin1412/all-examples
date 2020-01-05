# -*- coding: utf-8 -*-

import json
import scrapy
from scrapy_examples.spiders import BaseRedisSpider

REDIS_CONF = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 0,
    "password": ""
}

class DemoSpider(BaseRedisSpider):
    '''
    scrapy crawl demo

    lpush demo:start_urls '{"key":"value"}'
    '''

    name = 'demo'
    # allowed_domains = ['demo.com']
    custom_settings = {
        'REDIS_URL': 'redis://:{password}@{host}:{port}/{db}'.format(**REDIS_CONF),
        'CONCURRENT_REQUESTS': 50,
        'REDIS_START_URLS_BATCH_SIZE': 50,
        'REDIS_START_URLS_KEY': '%(name)s:start_urls',
        'SCHEDULER': 'scrapy_redis.scheduler.Scheduler',
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter',
        'SCHEDULER_QUEUE_CLASS': 'scrapy_redis.queue.PriorityQueue',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_examples.middlewares.ChangeUrlMiddleware': 100,
        },
        # 'ITEM_PIPELINES': {
        # },
        # 'LOG_LEVEL': logging.INFO,
        # 'DOWNLOAD_TIMEOUT': 5,
        # 'DOWNLOAD_DELAY': 0.03,
        # 'RANDOMIZE_DOWNLOAD_DELAY': False,
        # 改变url长度限制
        # 'URLLENGTH_LIMIT': 5000,   
    }

    def __init__(self, name=None, **kwargs):
        '''某些情况下需要重写该方法'''
        super(DemoSpider, self).__init__(name, **kwargs)
        self.url = "http://www.demo.com/?key={}"

    def make_requests_from_url(self, data: str):
        '''
        必须有以下两个字段, 其它字段根据业务需要自定
        {
            "key": "value"
        }
        '''
        try:
            self.logger.info(f'receive task: {data}')
            data = json.loads(data)

            value = data['key']

            url = self.url.format(value)

            # get 请求
            return scrapy.Request(
                url,
                dont_filter=True,
                priority=0,
                meta=data
            )

            """
            # post Form请求
            post_data = {}
            return scrapy.FormRequest(
                url=url,
                callback=self.parse,
                dont_filter=True,
                formdata=post_data,
                headers={},
                priority=0,
                meta=data
            )

            # post json请求
            post_data = {}
            return scrapy.Request(
                url=url,
                method='POST',
                callback=self.parse,
                dont_filter=True,
                body=json.dumps(post_data),
                headers={'Content-Type': 'application/json'},
                priority=0,
                meta=data
            )
            """
        except Exception as e:
            self.logger.exception(f"parse req data error, data: {data}  error: {str(e)}")

    def parse(self, response):
        self.logger.debug(response.url)
