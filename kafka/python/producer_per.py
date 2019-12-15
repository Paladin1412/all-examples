# -*- coding: utf-8 -*-

'''
producer performance

environment:
    mac
    python3.7
    broker 1
    partition 2
'''

import json
import time
from kafka import KafkaProducer

topic = 'demo'
nums = 1000000


def main():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda m: json.dumps(m).encode('utf-8')
    )
    st = time.time()
    cnt = 0
    for _ in range(nums):
        producer.send(topic, value=_)
        cnt += 1
        if cnt % 10000 == 0:
            print(cnt)

    producer.flush()

    et = time.time()
    cost_time = et - st
    print('send nums: {}, cost time: {}, rate: {}/s'.format(nums, cost_time, nums // cost_time))


if __name__ == '__main__':
    main()

'''
send nums: 1000000, cost time: 61.89236712455749, rate: 16157.0/s
send nums: 1000000, cost time: 61.29534196853638, rate: 16314.0/s
'''
