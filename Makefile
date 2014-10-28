### Makefile --- 

## Author: shell@debws0.lan
## Version: $Id: Makefile,v 0.0 2014/10/27 03:25:19 shell Exp $
## Keywords: 
## X-URL: 
# time, cpu time, context switch, read, write, memory, cpu usage.

TIMES=1000000000

all: perform_call

clean:
	rm -rf perf_call perf_syscall perf_fork perf_thread

perform_%: perf_%
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES)
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES)
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES)

perf_%: perf_%.c
	gcc -pthread -o $@ $^

### Makefile ends here
