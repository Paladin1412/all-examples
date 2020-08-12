# -*- coding: utf-8 -*-

'''
scrapy crawl example
'''

import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
        },
        'ITEM_PIPELINES': {
            'aliyun_oss.pipelines.AliyunOssPipeline': 100,
        },
        'DOWNLOAD_DELAY': 1,
    }

    def start_requests(self):
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'zh,en;q=0.9,pt;q=0.8,pl;q=0.7,zh-CN;q=0.6',
        }
        yield scrapy.Request(
            'https://movie.douban.com/top250',
            headers=headers,
            callback=self.parse
        )

    def parse(self, response):
        movie_images = response.xpath('//img/@src').extract()
        item = {
            "image_urls": movie_images[:5]
        }
        yield item
