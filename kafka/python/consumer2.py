# -*- coding: utf-8 -*-

'''
消费者: 指定group_id

测试结果:
1. 消费者必须 <= 分区数, 不同消费者收到的消息不同
2. auto_offset_reset='latest'
    - 新group_id: 只消费启动后的收到的数据, 重启后会从上次提交offset的地方开始消费, 保证不丢失这段时间内的数据
    - 旧group_id: 从上次提交offset的地方开始消费
3. auto_offset_reset='earliest'
    - 新group_id: 会消费全量数据
    - 旧group_id: 从上次提交offset的地方开始消费
'''

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
        # auto_offset_reset='latest',
        auto_offset_reset='earliest',
        group_id=group_id,

    )
    for msg in consumer:
        print(msg)
        print(msg.value)

    consumer.close()


if __name__ == '__main__':
    main()
