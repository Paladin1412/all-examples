# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.exceptions import NotConfigured
from scrapy.pipelines.images import ImagesPipeline

default_headers = {
    'accept': 'image/webp,image/*,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, sdch, br',
    'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'cookie': 'bid=yQdC/AzTaCw',
    'referer': 'https://www.douban.com/photos/photo/2370443040/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
}

################################
# 阿里云oss

import os
import oss2
from scrapy.log import logger


class AliOssStore(object):
    def __init__(self, access_key, access_secret, host_base, bucket_name):
        """

        :param access_key:
        :param access_secret:
        :param host_base:
        :param bucket_name:
        """
        auth = oss2.Auth(access_key, access_secret)
        self._bucket = oss2.Bucket(auth, host_base, bucket_name)

    def stat_file(self, path, info):
        # always return the empty result ,force the media request to download the file
        return {}

    def persist_file(self, path, buf, info, meta=None, headers=None):
        """Upload file to Ali oss storage"""
        self._upload_file(path, buf)

    def _upload_file(self, path, buf):
        self._bucket.put_object(key=path, data=buf.getvalue())
        logger.info('upload the image {} done!'.format(path))


################################


class AliyunOssPipeline(ImagesPipeline):

    def __init__(self, ali_oss_config):
        self.ali_oss_config = ali_oss_config
        self.folder = ali_oss_config.get('folder', '')
        super(AliyunOssPipeline, self).__init__(ali_oss_config)

    @classmethod
    def from_settings(cls, settings):
        ali_oss_config = settings.getdict('ALI_OSS_CONFIG', {})
        if not ali_oss_config:
            raise NotConfigured('Please check ALI_OSS_CONFIG to enable this pipeline')

        return cls(ali_oss_config)

    def _get_store(self, uri):
        store = AliOssStore(
            self.ali_oss_config['access_key'],
            self.ali_oss_config['access_secret'],
            self.ali_oss_config['host_base'],
            self.ali_oss_config['bucket_name']
        )
        return store

    def get_media_requests(self, item, info):
        requests = []
        for x in item.get(self.images_urls_field, []):
            requests.append(scrapy.Request(
                x,
                headers=default_headers
            ))
        return requests

    def file_path(self, request, response=None, info=None):
        """
        define the image path interface

        :param request:
        :param response:
        :param info:
        :return:
        """
        img_path = super(AliyunOssPipeline, self).file_path(request, response, info)
        # the image path will like this full/abc.jpg ,we just need the image name
        image_name = img_path.rsplit('/', 1)[-1] if '/' in img_path else img_path
        if self.folder:
            image_name = os.path.join(self.folder, image_name)

        return image_name
