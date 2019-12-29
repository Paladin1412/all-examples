package main

import (
	"context"
	"github.com/segmentio/kafka-go"
	"log"
	"strconv"
	"time"
)

func init() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)
}

func main() {
	log.Println("starting ...")
	// 转换为ms
	st := time.Now().UnixNano() / 1e6
	const test_nums = 1000000

	config := kafka.WriterConfig{
		Brokers:      []string{"localhost:9092"},
		Topic:        "demo",
		Balancer:     &kafka.RoundRobin{},
		Async:        true,
		RequiredAcks: -1,
	}

	producer := kafka.NewWriter(config)

	for i := 0; i < test_nums; i++ {
		msg := kafka.Message{
			Value: []byte(strconv.Itoa(i)),
		}
		err := producer.WriteMessages(context.Background(), msg)
		if err != nil {
			log.Printf("error msg: %v\n", msg)
		}
		//log.Printf("send %d\n", i)
	}

	producer.Close()

	et := time.Now().UnixNano() / 1e6
	cost_time := float64(et-st) / 1000
	log.Printf("End !  cost time: %v, avg rate: %v", cost_time, test_nums/cost_time)
}

// End !  cost time: 1.305, avg rate: 766283.5249042145
// End !  cost time: 1.359, avg rate: 735835.1729212656
// End !  cost time: 1.307, avg rate: 765110.9410864576