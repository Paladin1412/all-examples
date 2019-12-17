# -*- coding: utf-8 -*-

'''
callback也是保证分区有序的, 比如2条消息, a先发送, b后发送, 对于同一个分区, 那么会先回调a的callback, 再回调b的callback
'''

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
    # close() 方法会阻塞等待之前所有的发送请求完成后再关闭 KafkaProducer
    producer.close()


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
    # close() 方法会阻塞等待之前所有的发送请求完成后再关闭 KafkaProducer
    producer.close()


if __name__ == '__main__':
    # main()
    main2()
