#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Wed Mar  7 09:52:30 CET 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: draw2Dh.py -*-
# -*- purpose: -*-
 
'''
Module docstring
'''

import os
import argparse 

import matplotlib.pyplot as plt

from pyhisto.histogram2D import Histogram2D as h2d


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Histo to image converter (uses matplotlib)')
    parser.add_argument('--outext', type=str,
                        default='.png', nargs='?',
                        help="Extension of image file")
    parser.add_argument('--xmin', type=float, 
                        default=-1, nargs='?', 
                        help='minimum on x axis')
    parser.add_argument('--xmax', type=float, 
                        default=-1, nargs='?', 
                        help='maximum on x axis')
    parser.add_argument('--ymin', type=float, 
                        default=-1, nargs='?', 
                        help='minimum on y axis')
    parser.add_argument('--ymax', type=float, 
                        default=-1, nargs='?', 
                        help='maximum on y axis')
    parser.add_argument("--grid", help="show the grid",
                        action="store_true")
    parser.add_argument("--size", nargs='?', default="(25,12)",
                        type=str,
                        help="Size of the figure")
    parser.add_argument('files', type=str,
                        nargs='*', help="Faster files to read")
    args = parser.parse_args()

    for f in args.files:
        if os.path.exists(f) and os.path.isfile(f):
            h = h2d(fromstring=open(f, 'r').read())
            fig = plt.figure(figsize=eval(args.size))
            plt.figure(figsize=(15,10))
            plt.grid(args.grid)
            plt.pcolormesh(*h.xyz())
            plt.colorbar()
            plt.savefig(f+args.outext)
            plt.close('all')

            
