package main

import (
	"flag"
	"fmt"
	"runtime"
	"strconv"
)

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

	for i := 0; i < c; i++ {
		go goroutine_gosched(n, ch_end)
	}

	for i := 0; i < c; i++ {
		<-ch_end
	}
	return
}
