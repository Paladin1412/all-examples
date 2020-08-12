package main

// 指定group_id, 消费者重启后可以继续从上一次结束的地方进行消费

import (
	"context"
	"github.com/segmentio/kafka-go"
	"log"
	"time"
)

func init() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)
}

func main() {
	log.Println("start ...")
	const test_nums = 1000000
	st := time.Now().UnixNano() / 1e6

	config := kafka.ReaderConfig{
		Brokers: []string{"localhost:9092"},
		Topic:   "demo",
		GroupID: "spider1",
		// Partition不能和GroupId同时设置
		//Partition: 0,
		MinBytes:       10e3,
		MaxBytes:       10e6,
		CommitInterval: 100 * time.Microsecond,
	}
	cnt_consumer := 0
	consumer := kafka.NewReader(config)
	for {
		_, err := consumer.ReadMessage(context.Background())
		if err != nil {
			log.Println(err)
			break
		}
		cnt_consumer += 1
		if cnt_consumer >= test_nums {
			break
		}
		//log.Printf("[message at topic:%v partition:%v offset:%v] value:%s\n", msg.Topic, msg.Partition, msg.Offset, string(msg.Value))
	}
	consumer.Close()

	et := time.Now().UnixNano() / 1e6
	cost_time := float64(et-st) / 1000
	log.Printf("End ! consumer nums: %d, cost time: %v, avg rate: %v", cnt_consumer, cost_time, test_nums/cost_time)
}

// End ! consumer nums: 1000000, cost time: 3.227, avg rate: 309885.3424233034
// End ! consumer nums: 1000000, cost time: 3.369, avg rate: 296823.9833778569
// End ! consumer nums: 1000000, cost time: 3.163, avg rate: 316155.54852987675
