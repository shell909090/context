#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2014-10-21
@author: shell.xu
'''
import os, sys, errno, socket, signal, threading, logging

# from ctypes import cdll
# libc = cdll.LoadLibrary('libc.so.6')

# 实际处理程序，只是简单的将输入吐回去
def echo(conn):
    while True:
        d = conn.recv(1024)
        if not d: return 0
        conn.sendall(d)

# http的仿真程序，只是简单的读到两个回车，然后吐出固定的返回
def httpmock(conn):
    # http://www.larsen-b.com/Article/221.html
    # libc.sched_setscheduler(0, )
    s = ''
    while True:
        d = conn.recv(1024)
        if not d: return 0
        s += d
        if '\r\n\r\n' in s: break
    conn.sendall('HTTP/1.1 200 OK\r\nContain-Length: 2\r\nConnection: close\r\n\r\nok')
    conn.close()
    return 0

threads = []
threads_lock = threading.Lock()
def do_sub_thread(f, s, conn):
    def inner():
        try: f(conn)
        finally:
            with threads_lock: threads.remove(th)
            logging.info('one thread end')
    th = threading.Thread(target=inner)
    with threads_lock: threads.append(th)
    th.start()
    logging.info('new thread run')
    return th

def thread_quit():
    while threads: threads[0].join()

def fork_start():
    def handler_chld(signum, frame):
        logging.info('some child died')
        try:
            # 此处使用循环是因为信号是一个标志位，并不保留发送个数，因而存在信号“丢失”问题
            while os.waitpid(-1, os.WNOHANG)[0]: pass
        except OSError: pass
    return signal.signal(signal.SIGCHLD, handler_chld)

def do_sub_fork(f, s, conn):
    pid = os.fork()
    # 子进程关闭listen端口，父进程关闭conn是常见手法
    if pid != 0:
        conn.close()
        logging.info('new child created')
        return pid
    s.close()
    rslt = f(conn)
    # 这里使用finally会阻断python对异常的进一步捕获，导致异常栈未打印
    # 而不使用finally的前提是上层堆栈不能有任何的异常捕获和处理流程，否则会导致上层代码执行
    # 另一个做法是此处的异常处理函数模拟栈打印流程
    os._exit(rslt)

def main():
    # logging.basicConfig(level=logging.INFO)
    # fork_start()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 1112))
    s.listen(5)
    while True:
        # 使用siginterrupt的话，由于重启了调用，因此实际进程在accept退出前不会触发信号中断
        try: conn, addr = s.accept()
        except socket.error as err:
            if err.errno == errno.EINTR: continue
            raise
        # do_sub_fork(httpmock, s, conn)
        do_sub_thread(httpmock, s, conn)
    thread_quit()
    
if __name__ == '__main__': main()
