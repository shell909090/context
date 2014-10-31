package main

import (
	"flag"
	"fmt"
	"strconv"
)

func goroutine_nil() {
}

func main() {
	flag.Parse()

	n, err := strconv.Atoi(flag.Arg(0))
	if err != nil {
		fmt.Printf("unknown number")
		return
	}

	for i := 0; i < n; i++ {
		go goroutine_nil()
	}
	return
}
