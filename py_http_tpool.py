#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2014-10-21
@author: shell.xu
'''
import os, sys, errno, socket, Queue, signal, threading, logging

# 实际处理程序，只是简单的将输入吐回去
def echo(conn):
    while True:
        d = conn.recv(1024)
        if not d: return 0
        conn.sendall(d)

# http的仿真程序，只是简单的读到两个回车，然后吐出固定的返回
def httpmock(conn):
    s = ''
    while True:
        d = conn.recv(1024)
        if not d: return 0
        s += d
        if '\r\n\r\n' in s: break
    conn.sendall('HTTP/1.1 200 OK\r\nContain-Length: 2\r\nConnection: close\r\n\r\nok')
    conn.close()
    return 0

class TPool(object):

    def __init__(self, n):
        self.size = n
        self.q = Queue.Queue(10000)
        self.threads = []
        for i in xrange(n):
            th = threading.Thread(target=self.starter)
            self.threads.append(th)
            th.daemon = True
            th.start()

    def call(self, func, *args):
        logging.info('put')
        self.q.put((func, args))

    def starter(self):
        while True:
            logging.info('wait get')
            func, args = self.q.get()
            logging.info('one req start')
            try: func(*args)
            finally:
                logging.info('one req end')
                self.q.task_done()

    def join(self):
        # while threads: threads[0].join()
        self.q.join()

def main():
    # logging.basicConfig(level=logging.INFO)
    pool = TPool(4)

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 1112))
    s.listen(5)
    while True:
        try: conn, addr = s.accept()
        except socket.error as err:
            if err.errno == errno.EINTR: continue
            raise
        pool.call(httpmock, conn)
    pool.join()
    
if __name__ == '__main__': main()
