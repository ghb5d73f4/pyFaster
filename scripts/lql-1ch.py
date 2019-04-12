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

from pyhisto import LazyHistogram2D as h2d
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
    parser.add_argument('--reflabel', type=int,
                        default=0, nargs='?',
                        required=True,
                        help="Time refrence label")
    parser.add_argument('--tnbins', type=int, 
                        default=1250, nargs='?', 
                        help='number of time bins in histogram')
    parser.add_argument('--tmin', type=float, 
                        default=-1000, nargs='?', 
                        help='minimum time in histogram')
    parser.add_argument('--tmax', type=float, 
                        default=4000,
                        nargs='?', 
                        help='maximum value in histogram')
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
    parser.add_argument('--coarseenbins', type=int,
                        default=1500, nargs='?',
                        help='Number of energy bins in coarse histogram')
    parser.add_argument('--coarsetnbins', type=int,
                        default=625, nargs='?',
                        help='Number of time bins in coarse histogram')
    parser.add_argument('--outputdir', type=str,
                        default='./output', nargs="?",
                        help="directory where to put the files")
    parser.add_argument('files', type=str,
                        nargs='*', help="Faster files to read")
    args = parser.parse_args()
    
    # define counters histogram
    hcounters = h1d(nbins=5, arraytype='d')
    # defines 2D histograms
    h2clean = h2d(args.tnbins, args.tmin, args.tmax,
                  args.enbins, args.emin, args.emax)
    h2all = h2d(args.coarsetnbins, args.tmin, args.tmax,
                args.coarseenbins, args.emin, args.emax)
    counter_label = args.label+1000
    try:
        pass
        ref_time = 0

        for f in args.files:
            for evt in faster.FileReader(f, args.nmax):
                if evt.type_alias==10:
                # first, find the time of reference
                    ref_time = next( _.time for _ in evt.data['events'] if _.label==args.reflabel)
                    for subevt in evt.data.get('events', tuple()):
                        if subevt.label==args.label:
                            tof=subevt.time-ref_time
                            h2all.fast_fill(tof, subevt.data.get('value', -1.))
                            hcounters.fast_fill(3, 1)
                            if (subevt.data.get('pileup', 0)==0 and
                                subevt.data.get('saturated', 0)==0 ):
                                h2clean.fast_fill(tof, subevt.data.get('value', -1.))
                                hcounters.fast_fill(4,1)
                                pass
                            #end if clean
                            pass
                        #end if label
                        pass
                    #end for
                    pass
                elif evt.type_alias==70:
                    if evt.label==counter_label:
                        hcounters.fast_fill(1, evt.data.get('calc', 0))
                        hcounters.fast_fill(2, evt.data.get('sent', 0))
                        hcounters.fast_fill(0, evt.data.get('trig', 0))
                #end if type_alias
                
                pass
            #end for FileReader
            pass
        #end for files
        # Use MAP and label to determine the output files (3: clean, all and counters)
        channel_name = MAP[args.label]
        open("".join([args.outputdir, "/", channel_name, ".clean.2d.txt"]),
             'w').write(str(h2clean))
        open("".join([args.outputdir, "/", channel_name, ".all.2d.txt"]),
             'w').write(str(h2all))
        open("".join([args.outputdir, "/", channel_name, ".counters.1d.txt"]),
             'w').write(str(hcounters))
    except KeyboardInterrupt:
        #ignore 
        pass 
