# -*- coding: utf-8 -*-

import json
from kafka import KafkaProducer

topic = 'demo'


def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


def on_send_error(excp):
    print('I am an errback: {}'.format(excp))


def main():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092'
    )
    producer.send(topic, value=b'{"test_msg":"hello world"}').add_callback(on_send_success).add_callback(
        on_send_error)
    producer.flush()


def main2():
    '''
    发送json格式消息
    :return:
    '''
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda m: json.dumps(m).encode('utf-8')
    )
    producer.send(topic, value={"test_msg": "hello world"}).add_callback(on_send_success).add_callback(
        on_send_error)
    producer.flush()


if __name__ == '__main__':
    # main()
    main2()
