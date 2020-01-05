package main

// 指定group_id, 消费者重启后可以继续从上一次结束的地方进行消费

import (
	"context"
	"github.com/segmentio/kafka-go"
	"log"
)

func init() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)
}

func main() {
	log.Println("start ...")

	config := kafka.ReaderConfig{
		Brokers: []string{"localhost:9092"},
		Topic:   "demo",
		GroupID: "spider1",
		// Partition不能和GroupId同时设置
		//Partition: 0,
		MinBytes:       10e3,
		MaxBytes:       10e6,
		CommitInterval: 5,
	}

	consumer := kafka.NewReader(config)
	for {
		msg, err := consumer.ReadMessage(context.Background())
		if err != nil {
			log.Println(err)
			break
		}
		log.Printf("[message at topic:%v partition:%v offset:%v] value:%s\n", msg.Topic, msg.Partition, msg.Offset, string(msg.Value))
	}
	consumer.Close()
	log.Println("End !")
}
