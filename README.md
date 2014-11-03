# 项目简介

测试各种context switch的性能和环境对性能的影响。

# 文件命名

s\_打头的是单线程模式c代码，t\_打头的是多线程模式c代码:

* s_call: 调用开销
* s_syscall: 内核调用开销
* s_fork: 进程fork开销
* t_thread: 线程create开销
* t_cs: 线程切换开销

py\_打头是python代码:

* py_greenlet: python下greenlet性能测试
* py_yield: python下yield性能测试
* http\_fork\_thread: 进城/线程模式http服务器
* http\_tpool: 线程池模式http服务器

g\_打头的是golang测试代码:

* g_chan: chan模式性能
* g_goroutine: goroutine生成销毁开销(TODO: 注意，未必等待完成)
* g_sched: sched模式性能

h\_打头的是辅助代码:
