package main

import (
	"context"
	"github.com/segmentio/kafka-go"
	"log"
	"strconv"
)

func init() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)
}

func main() {
	log.Println("starting ...")

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
			log.Printf("error msg: %v\n", msg)
		}
		log.Printf("send %d\n", i)
	}

	producer.Close()
	log.Println("End !")
}
