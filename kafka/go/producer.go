package main

import (
	"context"
	"fmt"
	"github.com/segmentio/kafka-go"
	"strconv"
)

func main() {
	fmt.Println("start ...")

	config := kafka.WriterConfig{
		Brokers:  []string{"localhost:9092"},
		Topic:    "demo",
		Balancer: &kafka.RoundRobin{},
		Async:    true,
	}

	producer := kafka.NewWriter(config)

	for i := 0; i < 10; i++ {
		msg := kafka.Message{
			Value: []byte(strconv.Itoa(i)),
		}
		err := producer.WriteMessages(context.Background(), msg)
		if err != nil {
			fmt.Printf("error msg: %v\n", msg)
		}
		fmt.Printf("send %d\n", i)
	}

	producer.Close()
	fmt.Println("End !")
}
