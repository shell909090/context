### Makefile --- 

## Author: shell@debws0.lan
## Version: $Id: Makefile,v 0.0 2014/10/27 03:25:19 shell Exp $
## Keywords: 
## X-URL: 
# time, cpu time, context switch, read, write, memory, cpu usage.

TIMES=100000000
THREADS=1

all: perform_t_cs

clean:
	rm -rf s_call s_syscall s_fork t_thread t_cs

perform_yield: py_yield.py
	python $< 100000000

perform_greenlet: py_greenlet.py
	python $< 10000000 100

perform_t_cs: t_cs
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES) $(THREADS)
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES) $(THREADS)
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES) $(THREADS)

perform_%: %
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES)
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES)
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES)

s_%: s_%.c
	gcc -o $@ $^

t_%: t_%.c
	gcc -pthread -o $@ $^

### Makefile ends here
