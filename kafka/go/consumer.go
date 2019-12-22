package main

import (
	"fmt"
	"github.com/Shopify/sarama"
	"strings"
)

func main() {
	const topic = "demo"
	const group = "test0"
	const kafka_server = "127.0.0.1:9092"

	config := sarama.NewConfig()
	config.Consumer.Group.Rebalance.Strategy = sarama.BalanceStrategyRoundRobin
	config.Consumer.Offsets.Initial = sarama.OffsetNewest

	//创建消费者
	consumer, err := sarama.NewConsumerGroup(strings.Split(kafka_server, ","), group, config)
	if err != nil {
		fmt.Println("Error creating consumer group client: %v", err)
		return
	}

}
