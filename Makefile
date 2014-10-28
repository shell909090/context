### Makefile --- 

## Author: shell@debws0.lan
## Version: $Id: Makefile,v 0.0 2014/10/27 03:25:19 shell Exp $
## Keywords: 
## X-URL: 

all: perform_fork

clean:
	rm -rf perform_fork perform_thread

perform_fork: perf_fork
# time, cpu time, context switch, read, write, memory, cpu usage.
	time -f "%e,%S,%c,%r,%s,%K,%P" ./perf_fork 1000000
	time -f "%e,%S,%c,%r,%s,%K,%P" ./perf_fork 1000000
	time -f "%e,%S,%c,%r,%s,%K,%P" ./perf_fork 1000000

perf_fork: perf_fork.c
	gcc -o $@ $^

perform_thread: perf_thread
	time -f "%e,%S,%c,%r,%s,%K,%P" ./perf_thread 1000000
	time -f "%e,%S,%c,%r,%s,%K,%P" ./perf_thread 1000000
	time -f "%e,%S,%c,%r,%s,%K,%P" ./perf_thread 1000000

perf_thread: perf_thread.c
	gcc -pthread -o $@ $^

### Makefile ends here
