'''
Compute an histogram of delta_t between a reference channel and a label

Usage:
 $ fasterDeltat.py --label=% --reflabel=% [--tmin=%] [--tmax=%] [--nbins=% [--nmax=%] ]file.fast 
'''

import sys,os

import argparse

import faster

from pyhisto import LazyHistogram2D as h2d 

def faster2bidim(files,
                 label=0, reflabel=0,
                 nmax=faster.const.max_number_of_events_in_file,
                 ntbins=100, tmin=-25000, tmax=65000,
                 nebins=1000, emin=0, emax=300000):
    '''Return a delta t histogram from files'''
    try:
        hbidim = h2d(ntbins, tmin, tmax,
                     nebins, emin, emax)
        ref_time = 0
                
        for f in files:
            for evt in faster.FileReader(f, nmax):
                if evt.type_alias==10:
                    # first, find the time of reference
                    ref_time = next( _.time for _ in evt.data['events'] if _.label==reflabel)
                    for subevt in evt.data['events']:
                        if subevt.label==label:
                            hbidim.fast_fill(subevt.time-ref_time,
                                             subevt.data.get('value', -1.))
            #end for evt
        #end for f
        return hbidim                     
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)  
    

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
    parser.add_argument('--ntbins', type=int, 
                        default=100, nargs='?', 
                        help='number of time bins in histogram')
    parser.add_argument('--tmin', type=float, 
                        default=-25000, nargs='?', 
                        help='minimum time in histogram')
    parser.add_argument('--tmax', type=float, 
                        default=65000,
                        nargs='?', 
                        help='maximum value in histogram')
    parser.add_argument('--nebins', type=int, 
                        default=1000, nargs='?', 
                        help='number of energy bins in histogram')
    parser.add_argument('--emin', type=float, 
                        default=0.0, nargs='?', 
                        help='minimum energy in histogram')
    parser.add_argument('--emax', type=float, 
                        default=300000,
                        nargs='?', 
                        help='maximum valueenergy in histogram')
    parser.add_argument('files', type=str,
                        nargs='*', help="Faster files to read")
    args = parser.parse_args()

    print(faster2bidim(args.files,
                       args.label, args.reflabel,
                       args.nmax,
                       args.ntbins, args.tmin, args.tmax,
                       args.nebins, args.emin, args.emax))
