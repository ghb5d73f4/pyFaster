#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Mar 13 14:09:01 CET 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: add1D -*-
# -*- purpose: -*-
 
'''
Module docstring
'''
import sys,os

#adding scripts path
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/lib")

import argparse

from pyhisto.histogram import Histogram as histo

if __name__=="__main__":
     parser = argparse.ArgumentParser(description='calibrate a 1D hisotgrams')
     parser.add_argument('--slope', type=float, nargs='?',
                         default=1.0,
                         help="slope")
     parser.add_argument('--offset', type=float, 
                         default=0., nargs='?',
                         help="offset")
     parser.add_argument('file', type=str,
                         nargs='?',
                         help="histogram.1d.txt file to read and calibrate")
     args = parser.parse_args()
     if os.path.exists(args.file) and os.path.isfile(args.file):
         h = histo(fromfile=args.file)
         for b in h:
             b.lowedge = b.lowedge*args.slope + args.offset
             b.upedge = b.upedge*args.slope + args.offset
             b.upedge, b.lowedge = max(b.upedge, b.lowedge), min(b.upedge, b.lowedge)
         h._frombins(h.bins)
         print(h)

