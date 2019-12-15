# -*- coding: utf-8 -*-

'''
consumer performance
'''

import time
from kafka import KafkaConsumer

topic = 'demo'
group_id = 'test_id'


def main1():
    nums = 0
    st = time.time()

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        group_id=group_id
    )
    for msg in consumer:
        nums += 1
        if nums >= 500000:
            break
    consumer.close()

    et = time.time()
    cost_time = et - st
    print('one_by_one: consume nums: {}, cost time: {}, rate: {}/s'.format(nums, cost_time, nums // cost_time))


def main2():
    nums = 0
    st = time.time()

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        group_id=group_id
    )
    running = True
    batch_pool_nums = 1
    while running:
        batch_msgs = consumer.poll(timeout_ms=1000, max_records=batch_pool_nums)
        if not batch_msgs:
            continue
        for tp, msgs in batch_msgs.items():
            nums += len(msgs)
            if nums >= 500000:
                running = False
                break

    consumer.close()

    et = time.time()
    cost_time = et - st
    print('batch_pool: max_records: {} consume nums: {}, cost time: {}, rate: {}/s'.format(batch_pool_nums, nums,
                                                                                           cost_time,
                                                                                           nums // cost_time))


if __name__ == '__main__':
    # main1()
    main2()

'''
one_by_one: consume nums: 500000, cost time: 8.018627166748047, rate: 62354.0/s
one_by_one: consume nums: 500000, cost time: 7.698841094970703, rate: 64944.0/s


batch_pool: max_records: 1 consume nums: 500000, cost time: 17.975456953048706, rate: 27815.0/s
batch_pool: max_records: 1 consume nums: 500000, cost time: 16.711708784103394, rate: 29919.0/s

batch_pool: max_records: 500 consume nums: 500369, cost time: 6.654940843582153, rate: 75187.0/s
batch_pool: max_records: 500 consume nums: 500183, cost time: 6.854053258895874, rate: 72976.0/s

batch_pool: max_records: 1000 consume nums: 500485, cost time: 6.504687070846558, rate: 76942.0/s
batch_pool: max_records: 1000 consume nums: 500775, cost time: 7.047331809997559, rate: 71058.0/s
'''
