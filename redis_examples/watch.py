# -*- coding: utf-8 -*-

'''
模拟账户余额并发变动

使用redis的 watch 来实现乐观锁
'''

import redis


def key_for(user_id):
    return "account_{}".format(user_id)


def double_account(client, user_id):
    key = key_for(user_id)
    while True:
        pipe = client.pipeline(transaction=True)
        # 先监听, 再get
        pipe.watch(key)
        value = int(pipe.get(key))
        value *= 2  # 加倍

        # watch必须在事务开始前
        pipe.multi()
        pipe.set(key, value)
        try:
            pipe.execute()
            break  # 总算成功了
        except redis.WatchError:
            continue  # 事务被打断了，重试
    return int(client.get(key))  # 重新获取余额


client = redis.StrictRedis(decode_responses=True)

user_id = "abc"
client.setnx(key_for(user_id), 5)  # setnx 做初始化
print(double_account(client, user_id))
