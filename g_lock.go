package main

import (
	"flag"
	"fmt"
	"strconv"
	"sync"
)

func goroutine_lock(n int, mu *sync.Mutex, ch_end chan int) {
	mu.Lock()
	for i := 0; i < n; i++ {
		mu.Unlock()
		mu.Lock()
	}
	mu.Unlock()
	ch_end <- 1
}

func main() {
	flag.Parse()

	n, err := strconv.Atoi(flag.Arg(0))
	if err != nil {
		fmt.Printf("unknown number")
		return
	}

	c, err := strconv.Atoi(flag.Arg(1))
	if err != nil {
		fmt.Printf("unknown concurrent")
		return
	}

	ch_end := make(chan int, 100)

	var mu sync.Mutex
	for i := 0; i < c; i++ {
		go goroutine_lock(n, &mu, ch_end)
	}

	for i := 0; i < c; i++ {
		<-ch_end
	}
	return
}
