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
		mu.Unlock() // 这里是先执行被解锁上下文，还是先执行原始上下文？
		mu.Lock()   // 如果执行原始上下文，执行到这里就会锁定并发生上下文调度，因此是一次调度。
	}
	// 而如果先执行被解锁上下文，切去要一次，执行到所有goroutine均处于unlock位置后
	// 开始第一个lock。于是第一个goroutine执行完，再执行第二个goroutine，依次执行完。
	// 个人倾向于Unlock先不发生cs。
	// cs总是懒惰的
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
