### Makefile --- 

## Author: shell@debws0.lan
## Version: $Id: Makefile,v 0.0 2014/10/27 03:25:19 shell Exp $
## Keywords: 
## X-URL: 
# time, kernel time, context switch, read, write, memory, cpu usage.

TIMES=10000000

all: g_sched.txt

clean:
	rm -rf s_call s_syscall s_fork t_thread t_cs
	rm -rf g_chan g_goroutine g_sched

cleandata:
	rm -rf t_cs.txt t_cs.png
	rm -rf g_chan.txt g_chan.png g_sched.txt g_sched.png

perform_yield: py_yield.py
	python $< 100000000

perform_greenlet: py_greenlet.py
	python $< 10000000 100

t_cs.txt: t_cs
	python h_cs.py -e 16384 -m 10000 ./%< $@

g_chan.txt: g_chan
	python h_cs.py -c 1 -e 1048576 -m 1024 ./%< $@

g_sched.txt: g_sched
	python h_cs.py -c 1 -e 1048576 -m 1024 ./%< $@

perform_%: %
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES)
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES)
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES)

%.png: %.txt
	python h_draw.py $^ $@

g_%: g_%.go
	go build -o $@ $^

s_%: s_%.c
	gcc -o $@ $^

t_%: t_%.c
	gcc -pthread -o $@ $^

### Makefile ends here
