### Makefile --- 

## Author: shell@debws0.lan
## Version: $Id: Makefile,v 0.0 2014/10/27 03:25:19 shell Exp $
## Keywords: 
## X-URL: 
# time, cpu time, context switch, read, write, memory, cpu usage.

TIMES=1000000
THREADS=2

all: perform_fork

clean:
	rm -rf perf_call perf_syscall perf_fork perf_thread

perform_yield:
	python perf_yield.py 100000000

perform_greenlet:
	python perf_greenlet.py 10000000 100

perform_cs: perf_cs
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES) $(THREADS)
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES) $(THREADS)
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES) $(THREADS)

perform_%: perf_%
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES)
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES)
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES)

perf_%: perf_%.c
	gcc -o $@ $^

perf_thread: perf_thread.c
	gcc -pthread -o $@ $^

### Makefile ends here
