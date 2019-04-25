#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Fri Mar 29 14:22:29 CET 2019 -*-
# -*- copyright: GH/IPHC 2019 -*-
# -*- file: lql-1ch.py -*-
# -*- purpose: -*-
 
'''
Lexeme Quicker Lector - 1 channel 
'''
import sys,os

import argparse

#adding scripts path
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/lib")

import faster

from pyhisto import LazyHistogram as h1d

from grapheme import MAP

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Faster to Histo converter')
    parser.add_argument('--nmax', type=int, 
                        default=faster.const.max_number_of_events_in_file, nargs='?', 
                        help='maximum number of event to read')
    parser.add_argument('--label', type=int,
                        default=0, nargs='?',
                        required=True,
                        help="Label to read")
    parser.add_argument('--enbins', type=int, 
                        default=30000, nargs='?', 
                        help='number of energy bins in histogram')
    parser.add_argument('--emin', type=float, 
                        default=0.0, nargs='?', 
                        help='minimum energy in histogram')
    parser.add_argument('--emax', type=float, 
                        default=150000,
                        nargs='?', 
                        help='maximum valueenergy in histogram')
    parser.add_argument('--outputdir', type=str,
                        default='./output', nargs="?",
                        help="directory where to put the files")
    parser.add_argument('files', type=str,
                        nargs='*', help="Faster files to read")
    args = parser.parse_args()
    
    # define counters histogram
    hcounters = h1d(nbins=5, arraytype='d')
    # defines 2D histograms
    hclean = h1d(args.enbins, args.emin, args.emax, arraytype='L')
    hall = h1d(args.enbins, args.emin, args.emax, arraytype='L')
    counter_label = args.label+1000
    try:
        pass
        ref_time = 0

        for f in args.files:
            for evt in faster.FileReader(f, args.nmax):
                if evt.label==args.label:
                    hall.fast_fill(evt.data.get('value', -1.))
                    hcounters.fast_fill(3, 1)
                    if (evt.data.get('pileup', 0)==0 and
                        evt.data.get('saturated', 0)==0 ):
                        hclean.fast_fill(evt.data.get('value', -1.))
                        hcounters.fast_fill(4,1)
                        pass
                    #end if clean
                elif evt.label==counter_label:
                    hcounters.fast_fill(1, evt.data.get('calc', 0))
                    hcounters.fast_fill(2, evt.data.get('sent', 0))
                    hcounters.fast_fill(0, evt.data.get('trig', 0))
                #end if label
                pass
            #end for FileReader
            pass
        #end for files
        # Use MAP and label to determine the output files (3: clean, all and counters)
        channel_name = MAP[args.label]
        open("".join([args.outputdir, "/", channel_name, ".Eclean.1d.txt"]),
             'w').write(str(hclean))
        open("".join([args.outputdir, "/", channel_name, ".Eall.1d.txt"]),
             'w').write(str(hall))
        open("".join([args.outputdir, "/", channel_name, ".counters.1d.txt"]),
             'w').write(str(hcounters))
    except KeyboardInterrupt:
        #ignore 
        pass 
