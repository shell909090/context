#!/usr/bin/python
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

def test_yield(n):
    for i in call_yield(n): pass

def test_noyield(n):
    i = 0
    while i < n:
        i += 1

def main():
    n = int(sys.argv[1])
    t = timeit.Timer('test_yield(%d)' % n, 'from __main__ import test_yield')
    a = np.array(t.repeat(6, 1))
    print a.mean(), a.var()
    t = timeit.Timer('test_noyield(%d)' % n, 'from __main__ import test_noyield')
    a = np.array(t.repeat(6, 1))
    print a.mean(), a.var()
    
if __name__ == '__main__': main()
