#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2014-10-31
@author: shell.xu
'''
import os, sys, time, logging, subprocess
import numpy as np

CPUS     = 1
REPEAT   = 10
ACTIONS  = 1 << 20

def t_cs(execf, times, concurrent):
    time.sleep(0.2)
    output = subprocess.check_output(
        ['time', '-f', '%e', execf, '%d' % times, '%d' % concurrent],
        stderr=subprocess.STDOUT)
    return float(output.strip())

def t_cs_repeat(execf, times, concurrent, repeat):
    l = [t_cs(execf, times, concurrent) for i in xrange(repeat)]
    logging.debug(str(l))
    a = np.array(l)
    return a.mean(), a.var()

def cs_concurrent(execf, c):
    times = ACTIONS / c
    # if times < 1 << 14: times = 1 << 14
    f = 1000000000 * min(CPUS, c) / (times * c)
    logging.info('concurrent: %d, times: %d' % (c, times))
    m, v = t_cs_repeat(execf, times, c, REPEAT)
    m *= f
    v *= f
    return m, v

def exp(mi, ma, si):
    i = mi
    while i <= ma:
        yield i
        i *= si

def main():
    ''' h_cs.py execf start end outputfile '''
    # logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 5:
        print main.__doc__
        return

    execf = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    with open(sys.argv[4], 'w') as fo:
        for c in exp(start, end, 2):
            m, v = cs_concurrent(execf, c)
            print '%d, %f, %f' % (c, m, v)
            print >>fo, '%d, %f, %f' % (c, m, v)
            fo.flush()
    
if __name__ == '__main__': main()
