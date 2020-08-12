# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy_redis import defaults


class BaseRedisSpider(RedisSpider):
    def setup_redis(self, crawler=None):
        super(BaseRedisSpider, self).setup_redis(crawler)
        self.pipe = self.server.pipeline()

    def lpop_multi(self, redis_key, batch_size):
        self.pipe.lrange(redis_key, 0, batch_size - 1)
        self.pipe.ltrim(redis_key, batch_size, -1)
        datas, _ = self.pipe.execute()
        return datas

    def next_requests(self):
        """Returns a request to be scheduled or none."""
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', defaults.START_URLS_AS_SET)
        fetch_data = self.server.spop if use_set else self.lpop_multi
        # XXX: Do we need to use a timeout here?
        found = 0

        datas = fetch_data(self.redis_key, self.redis_batch_size)
        for data in datas:
            req = self.make_request_from_data(data)
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)
