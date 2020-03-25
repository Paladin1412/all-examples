# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-

'''
测试心跳超时情况
'''

import time
from kafka import KafkaConsumer

topic = 'demo'
group_id = 'test_id'


# group_id = 'test_id2'
# group_id = 'test_id3'
# group_id = 'test_id4'


def main():
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        # auto_offset_reset='earliest',
        group_id=group_id,

    )
    for msg in consumer:
        print(f'partition:{msg.partition}  value:{msg.value}')
        time.sleep(30)

    consumer.close()


if __name__ == '__main__':
    main()
