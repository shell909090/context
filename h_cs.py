#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2014-10-31
@author: shell.xu
'''
import os, sys, time, getopt, logging, subprocess
import numpy as np

CPUS     = 2
REPEAT   = 10
ACTIONS  = 1 << 20
MINTIMES = 1 << 10

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
    if times < MINTIMES: times = MINTIMES
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
    ''' h_cs.py execf outputfile
    -a: inital actions
    -c: cpus
    -e: ends concurrent
    -h: help
    -m: minimize action times
    -r: repeat time
    -s: starts concurrent
    '''
    optlist, args = getopt.getopt(sys.argv[1:], 'a:c:e:hm:r:s:')
    optdict = dict(optlist)
    if '-h' in optdict or len(args) < 2:
        print main.__doc__
        return

    if '-a' in optdict:
        global ACTIONS
        ACTIONS = int(optdict['-a'])
    if '-c' in optdict:
        global CPUS
        CPUS = int(optdict['-c'])
    if '-m' in optdict:
        global MINTIMES
        MINTIMES = int(optdict['-m'])
    if '-r' in optdict:
        global REPEAT
        REPEAT = int(optdict['-r'])

    start = int(optdict.get('-s', '0')) or 1
    end = int(optdict.get('-e', '0')) or 16384

    # logging.basicConfig(level=logging.INFO)

    execf = args[0]
    with open(args[1], 'w') as fo:
        for c in exp(start, end, 2):
            m, v = cs_concurrent(execf, c)
            print '%d, %f, %f' % (c, m, v)
            print >>fo, '%d, %f, %f' % (c, m, v)
            fo.flush()
    
if __name__ == '__main__': main()
