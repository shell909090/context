package main

import (
	"flag"
	"fmt"
	"runtime"
	"strconv"
)

func goroutine_chan(n int, ch chan int, ch_end chan int) {
	<-ch
	for i := 0; i < n; i++ {
		ch <- 1
		<-ch
	}
	ch <- 1
	ch_end <- 1
}

func goroutine_gosched(n int, ch_end chan int) {
	for i := 0; i < n; i++ {
		runtime.Gosched()
	}
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

	// for i := 0; i < c; i++ {
	// 	go goroutine_gosched(n, ch_end)
	// }

	ch := make(chan int, 1)
	for i := 0; i < c; i++ {
		go goroutine_chan(n, ch, ch_end)
	}
	ch <- 1

	for i := 0; i < c; i++ {
		<-ch_end
	}
	return
}
