# -*- coding: utf-8 -*-

'''
消费者: 指定group_id

测试结果:
1. pool 每次拉取只能拉取一个分区的消息, 比如有2个分区1个consumer, 那么会拉取2次
2. pool 是如果有消息马上进行拉取, 如果timeout_ms内没有新消息则返回空dict, 所以可能出现某次拉取了1条消息, 某次拉取了max_records条
'''

from kafka import KafkaConsumer

topic = 'demo'
group_id = 'test_id'


def main():
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        group_id=group_id,

    )
    while True:
        try:
            # return a dict
            batch_msgs = consumer.poll(timeout_ms=1000, max_records=33)
            if not batch_msgs:
                continue
            '''
            {TopicPartition(topic='demo', partition=0): [ConsumerRecord(topic='demo', partition=0, offset=42, timestamp=1576425111411, timestamp_type=0, key=None, value=b'74', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=2, serialized_header_size=-1)]}
            '''
            cnt = 0
            for tp, msgs in batch_msgs.items():
                cnt += len(msgs)
                print('topic: {}, partition: {} receive length: '.format(tp.topic, tp.partition, len(msgs)))
                for msg in msgs:
                    print(msg.value)

            print(f'batch_cnt:{cnt}')

        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == '__main__':
    main()
