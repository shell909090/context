### Makefile --- 

## Author: shell@debws0.lan
## Version: $Id: Makefile,v 0.0 2014/10/27 03:25:19 shell Exp $
## Keywords: 
## X-URL: 
# time, kernel time, context switch, read, write, memory, cpu usage.

TIMES=1000000000

all: perform_s_jmp

clean:
	rm -rf s_call s_syscall s_fork s_context s_jmp
	rm -rf t_thread t_sleep t_yield t_lock
	rm -rf g_chan g_goroutine g_sched g_lock

cleandata:
	rm -rf t_yield.txt t_yield.png t_lock.txt t_lock.png
	rm -rf g_chan.txt g_chan.png g_sched.txt g_sched.png g_lock.txt g_lock.png

perform_yield: py_yield.py
	python $< 100000000

perform_greenlet: py_greenlet.py
	python $< 10000000 100

t_sleep.txt: t_sleep
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES) 1
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES) 1
	@time -f "%e,%S,%c,%r,%s,%K,%P" ./$< $(TIMES) 1

t_yield.txt: t_yield
	python h_cs.py -e 16384 ./$< $@

t_lock.txt: t_lock
	python h_cs.py -e 16384 ./$< $@

g_chan.txt: g_chan
	python h_cs.py -c 1 -e 65536 ./$< $@

g_sched.txt: g_sched
	python h_cs.py -c 1 -e 65536 ./$< $@

g_lock.txt: g_lock
	python h_cs.py -c 1 -e 65536 ./$< $@

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
