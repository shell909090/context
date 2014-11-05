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
ACTIONS  = 1 << 24
MINTIMES = 10000

def t_cs(execf, times, concurrent):
    time.sleep(0.5)
    st = time.time()
    subprocess.call([execf, '%d' % times, '%d' % concurrent])
    return time.time() - st

def t_cs_repeat(execf, times, concurrent, repeat):
    l = [t_cs(execf, times, concurrent) for i in xrange(repeat)]
    logging.debug(str(l))
    a = np.array(l)
    return a.mean(), a.var()

def cs_concurrent(execf, c):
    times = ACTIONS / c
    if times < MINTIMES: times = MINTIMES

    logging.info('concurrent: %d, times: %d' % (c, times))
    m, v = t_cs_repeat(execf, times, c, REPEAT)
    if m < 1:
        times /= (m/2)
        logging.info('redo with m: %f, concurrent: %d, times: %d' % (m, c, times))
        m, v = t_cs_repeat(execf, times, c, REPEAT)

    f = 1000000000 * min(CPUS, c) / (times * c)
    m *= f
    v *= f
    return m, v

def runtest(execf, output, start, end):
    with open(output, 'w') as fo:
        c = start
        while c <= end:
            m, v = cs_concurrent(execf, c)
            logging.info('c: %d, time: %f(%f)' % (c, m, v))
            print >>fo, '%d, %f, %f' % (c, m, v)
            fo.flush()
            c *= 2

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

    logging.basicConfig(level=logging.INFO)
    runtest(args[0], args[1], start, end)
    
if __name__ == '__main__': main()
