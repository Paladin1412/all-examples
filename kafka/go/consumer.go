package main

import (
	"context"
	"fmt"
	"github.com/segmentio/kafka-go"
)

func main() {
	fmt.Println("start ...")

	config := kafka.ReaderConfig{
		Brokers: []string{"localhost:9092"},
		Topic:   "demo",
		GroupID: "spider1",
		// Partition不能和GroupId同时设置
		Partition: 0,
		MinBytes:  10e3,
		MaxBytes:  10e6,
		//StartOffset: 400,
		CommitInterval: 5,
	}

	consumer := kafka.NewReader(config)
	for {
		msg, err := consumer.ReadMessage(context.Background())
		if err != nil {
			fmt.Println(err)
			break
		}
		fmt.Printf("[message at topic:%v partition:%v offset:%v] value:%s\n", msg.Topic, msg.Partition, msg.Offset, string(msg.Value))
	}
	consumer.Close()
	fmt.Println("End !")
}
