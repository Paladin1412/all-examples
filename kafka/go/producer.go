package main

import (
	"fmt"
	"github.com/Shopify/sarama"
	"strconv"
)

func main() {
	const topic = "demo"
	const kafka_server = "127.0.0.1:9092"

	config := sarama.NewConfig()
	config.Producer.Retry.Max = 5
	// ack=1
	config.Producer.RequiredAcks = sarama.WaitForLocal
	config.Producer.Partitioner = sarama.NewRoundRobinPartitioner
	// if use sync producer, this must be true
	config.Producer.Return.Successes = true

	// use sync producer
	client, err := sarama.NewSyncProducer([]string{kafka_server}, config)
	if err != nil {
		fmt.Println("producer close, err:", err)
		return
	}
	defer client.Close()

	for i := 0; i < 10; i++ {
		// build message
		msg := &sarama.ProducerMessage{}
		msg.Topic = topic
		msg.Value = sarama.StringEncoder(strconv.Itoa(i))

		pid, offset, err := client.SendMessage(msg)
		if err != nil {
			fmt.Println("send message failed,", err)
			return
		}

		fmt.Printf("send msg: %v, pid:%v offset:%v\n", msg.Value, pid, offset)
	}

}
