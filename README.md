# 项目简介

测试各种context switch的性能和环境对性能的影响。

# 文件命名

s\_打头的是单线程模式c代码，t\_打头的是多线程模式c代码，py\_打头是python代码。

* call: 调用开销
* syscall: 内核调用开销
* fork: 进程fork开销
* thread: 线程create开销
* cs: 线程切换开销

* greenlet: python下greenlet性能测试
* yield: python下yield性能测试
