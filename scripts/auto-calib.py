#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Fri May  3 14:48:00 CEST 2019 -*-
# -*- copyright: GH/IPHC 2019 -*-
# -*- file: get_pileup_factor.py -*-
# -*- purpose: -*-
 
'''
Read an histogram and perform auto calibration
'''

import sys,os

#adding scripts path
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/lib")

import argparse

from pyhisto.histogram import Histogram as histo
#from pyhisto.tools import FindPeaks
from pyhisto.tools import GaussFit

from numpy import polyfit

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Autocalibration of an histogram')
    parser.add_argument('--slopeguess', type=float, nargs='?',
                        default=1.0,
                        help="guess for slope")
    parser.add_argument('--offsetguess', type=float, 
                        default=0., nargs='?', 
                        help='offset guess')
    parser.add_argument('--width', type=float, 
                        default=20.0, nargs='?', 
                        help='window size (in calibrated units')
    parser.add_argument("--force0", 
                        action='store_true',
                        help="force a (0.0) point in fit")
    parser.add_argument("--method", type=str,
                        default='max',
                        choices=['max', 'mean', 'fit'],
                        help="Metod used to determined the peak position")
    parser.add_argument("--energies", type=str,
                        default="",
                        help="file with list of energies")
    parser.add_argument('file', type=str,
                        nargs='?', help="histogram.1d.txt file to read")
    args = parser.parse_args()
    if os.path.exists(args.file) and os.path.isfile(args.file):
        h = histo(fromfile=args.file)
        energies = map(float, open(args.energies, 'r').readlines())
        points = []
        if args.force0:
            points.append( (0, 0) )
        for egamma in energies:
            channel_guess = int((egamma-args.offsetguess)/args.slopeguess)
            channel_window = ( int(channel_guess-args.width/args.slopeguess),
                               int(channel_guess+args.width/args.slopeguess) )
            hzoom = h.slice(*channel_window)
            print("# looking for {0} in {1}, {2}".format(egamma, *channel_window))
            the_position = hzoom[0].center()
            if args.method=='max':
                the_position = max(hzoom).center()
            elif args.method=='mean':
                print("Not implemented yet")
            elif args.method=='fit':
                the_position = GaussFit(hzoom).mean
            else:
                pass
            print("#     found {0}".format(the_position))
            points.append( (the_position, egamma) )
            pass
        #print(points)
        fitrslt = polyfit(*zip(*points), 1)
        print("""#autocalibration of {2}
#{3}
slope={0}
offset={1}""".format(*fitrslt, args.file, points))
        
# in bash, use
# ``cat data/vert/autocal.txt | grep offset | cut -d "=" -f 2`` to get the offset or slope 
