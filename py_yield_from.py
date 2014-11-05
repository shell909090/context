#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@date: 2014-10-28
@author: shell.xu
'''
import os, sys, timeit
import numpy as np

def call_yield(n):
    i = 0
    while i < n:
        yield i
        i += 1

def call_yield_loop(n, k):
    if k <= 1: yield from call_yield(n)
    else: yield from call_yield_loop(n, k-1)

def test_yield(n):
    for i in call_yield(n): pass

def test_yield_loop(n, k):
    for i in call_yield_loop(n, k): pass

def test_noyield(n):
    i = 0
    while i < n:
        i += 1

def main():
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    t = timeit.Timer('test_yield_loop(%d, %d)' % (n, k), 'from __main__ import test_yield_loop')
    a = np.array(t.repeat(6, 1))
    print(a.mean(), a.var())
    t = timeit.Timer('test_yield(%d, %d)' % n, 'from __main__ import test_yield')
    a = np.array(t.repeat(6, 1))
    print(a.mean(), a.var())
    t = timeit.Timer('test_noyield(%d)' % n, 'from __main__ import test_noyield')
    a = np.array(t.repeat(6, 1))
    print(a.mean(), a.var())
    
if __name__ == '__main__': main()
