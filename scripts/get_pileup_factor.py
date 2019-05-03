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

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Get Pile up factor ')
    parser.add_argument('file', type=str,
                        nargs='?', help="counter.1d.txt file to read")
    args = parser.parse_args()

    if os.path.exists(args.file) and os.path.isfile(args.file):
        h = histo(fromfile=args.file)
        n_trig = h[0].count
        n_sent = h[2].count
        n_all = h[3].count
        n_clean = h[4].count
        #print("# from trigger to sent : {0}".format(n_sent*1.0/n_trig))
        #print("# from all to clean : {0}".format(n_clean*1.0/n_all))
        print("cleanrate={0}".format(1.0*n_sent/n_trig*n_clean/n_all))
