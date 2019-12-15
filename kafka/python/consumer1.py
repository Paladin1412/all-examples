# -*- coding: utf-8 -*-

'''
消费者: group_id=None

测试结果:
1. 消费者可以大于分区数, 所有消费者都会收到消息
2. auto_offset_reset='earliest' 每次启动都会从最开始消费
3. auto_offset_reset='latest' 每次从最新的开始消费, 不会管哪些任务还没有消费
'''

from kafka import KafkaConsumer

topic = 'demo'


def main():
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        # auto_offset_reset='earliest',
    )
    for msg in consumer:
        print(msg)
        print(msg.value)

    consumer.close()


if __name__ == '__main__':
    main()
