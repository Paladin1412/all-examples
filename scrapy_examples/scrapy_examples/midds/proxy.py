# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import sys
import time
import base64
import random


class ProxyAbyMiddleware1(object):
    """
    阿布云代理
    """

    # 代理隧道验证信息
    proxyUser = ""
    proxyPass = ""

    proxyServer = "http://http-dyn.abuyun.com:9020"
    proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

    def process_request(self, request, spider):
        if not request.meta.get('dont_proxy'):
            pass
        else:
            request.meta["proxy"] = self.proxyServer
            request.headers["Proxy-Authorization"] = self.proxyAuth

    def process_response(self, request, response, spider):
        if request.meta.get('dont_proxy'):
            request.meta['dont_proxy'] = False
            return response
        else:
            if response.status == 429:
                return request
            return response


PY3 = sys.version_info[0] >= 3


def base64ify(bytes_or_str):
    if PY3 and isinstance(bytes_or_str, str):
        input_bytes = bytes_or_str.encode('utf8')
    else:
        input_bytes = bytes_or_str

    output_bytes = base64.urlsafe_b64encode(input_bytes)
    if PY3:
        return output_bytes.decode('ascii')
    else:
        return output_bytes


class Proxy16Middleware(object):
    '''
    16云
    '''

    proxyHost = ""
    proxyPort = ""

    # 代理隧道验证信息
    proxyUser = ""
    proxyPass = ""

    def process_request(self, request, spider):
        if request.meta.get('dont_proxy'):
            pass
        else:
            request.meta['proxy'] = f"http://{self.proxyHost}:{self.proxyPort}"

            # 添加验证头
            encoded_user_pass = base64ify(self.proxyUser + ":" + self.proxyPass)
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

            # 设置IP切换头(根据需求)
            tunnel = random.randint(1, 10000)
            request.headers['Proxy-Tunnel'] = str(tunnel)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_proxy'):
            request.meta['dont_proxy'] = False
            return response
        else:
            if response.status == 429:
                return request
            return response