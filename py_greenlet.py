#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2014-10-28
@author: shell.xu
'''
import os, sys, timeit
import greenlet
import numpy as np

def call_greenlet(grmain, n):
    i = 0
    while i < n:
        grmain.switch(i)
        i += 1
    return None

def test_greenlet(n):
    grmain = greenlet.getcurrent()
    gr = greenlet.greenlet(call_greenlet)
    i = gr.switch(grmain, n)
    while i is not None:
        i = gr.switch()

def test_greenlet1(k, n):
    if k > 0: return test_greenlet1(k-1, n)
    else: return test_greenlet(n)

def main():
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    t = timeit.Timer('test_greenlet(%d)' % n, 'from __main__ import test_greenlet')
    a = np.array(t.repeat(6, 1))
    print a.mean(), a.var()
    t = timeit.Timer('test_greenlet1(%d, %d)' % (k, n), 'from __main__ import test_greenlet1')
    a = np.array(t.repeat(6, 1))
    print a.mean(), a.var()
    
if __name__ == '__main__': main()
