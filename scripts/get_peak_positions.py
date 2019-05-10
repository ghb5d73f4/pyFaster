#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Fri May  3 14:48:00 CEST 2019 -*-
# -*- copyright: GH/IPHC 2019 -*-
# -*- file: get_pileup_factor.py -*-
# -*- purpose: -*-
 
'''
Read an counter histogram and compute the pile up factor
'''

import sys,os

#adding scripts path
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/lib")

import argparse

from pyhisto.histogram import Histogram as histo
from pyhisto.tools import FindPeaks

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Get peaks positions ')
    parser.add_argument('--npeaks', type=int, nargs='?',
                        default=1,
                        help="number of peaks to print")
    parser.add_argument('--width', type=float, nargs='?',
                        default=10.0,
                        help="width of peaks to find")
    parser.add_argument('--min', type=float, 
                        default=-1, nargs='?', 
                        help='minimum on x axis')
    parser.add_argument('--max', type=float, 
                        default=-1, nargs='?', 
                        help='maximum on x axis')
    parser.add_argument('file', type=str,
                        nargs='?', help="counter.1d.txt file to read")
    args = parser.parse_args()
    min_ = None if args.min==-1 else args.min
    max_ = args.max if args.max!=-1 else None
    if os.path.exists(args.file) and os.path.isfile(args.file):
        h = histo(fromfile=args.file).slice(min_, max_)
        pks = FindPeaks(h, args.npeaks, width=args.width)
        print(pks.peaks)
