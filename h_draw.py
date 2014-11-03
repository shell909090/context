#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2014-11-03
@author: shell.xu
'''
import os, sys, pprint
import Gnuplot

def readdata(filename):
    with open(filename) as fi:
        for line in fi:
            r = line.split(',')
            r = [i.strip() for i in r]
            r[0] = int(r[0])
            r[1] = float(r[1])
            r[2] = float(r[2])
            yield r

def colume_select(src, cols):
    for d in src:
        yield [d[c] for c in cols]

def draw(filename, output):
    pi = Gnuplot.Data(list(readdata(filename)),
                      with_='yerrorbar')
    g = Gnuplot.Gnuplot(debug=1)
    g.title('performance')
    g.xlabel('concurrent')
    g.ylabel('latency')
    g('set yrange [0:*]')
    g('set logscale x 2')
    g('set terminal png')
    g.set_string('output', output)
    g.plot(pi)

def main():
    draw(sys.argv[1], sys.argv[2])
    
if __name__ == '__main__': main()
