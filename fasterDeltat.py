'''
Compute an histogram of delta_t between a reference channel and a label

Usage:
 $ fasterDeltat.py --label=% --reflabel=% [--tmin=%] [--tmax=%] [--nbins=% [--nmax=%] ]file.fast 
'''

import sys,os

import argparse

import faster
from pyhisto import LazyHistogram as histo

def fasterDeltat(files,
                 label=0, reflabel=0,
                 nmax=faster.const.max_number_of_events_in_file,
                 nbins=1000, tmin=-25000, tmax=65000):
    '''Return a delta t histogram from files'''
    try:
        h1 = histo(args.nbins,
                   args.tmin, args.tmax)
        previous_ref_time = 0
                
        for f in args.files:
        
            for evt in faster.FileReader(f, args.nmax):
                if evt.label==args.label:
                    h1.fast_fill(evt.time-previous_ref_time)
                elif evt.label==args.reflabel:
                    previous_ref_time=evt.time
                elif evt.type_alias==10:
                    for subevt in evt.data['events']:
                        if subevt.label==args.reflabel:
                            previous_ref_time=subevt.time
                        elif subevt.label==args.label:
                            h1.fast_fill(subevt.time-previous_ref_time)
            #end for evt
        #end for f
        return h1                       
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)  
        print(sys.exc_info())
        print(__doc__)
    

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
    parser.add_argument('--nbins', type=int, 
                        default=1000, nargs='?', 
                        help='number of bins in histogram')
    parser.add_argument('--tmin', type=float, 
                        default=-25000, nargs='?', 
                        help='minimum time in histogram')
    parser.add_argument('--tmax', type=float, 
                        default=65000,
                        nargs='?', 
                        help='maximum value in histogram')
    parser.add_argument('files', type=str,
                        nargs='*', help="Faster files to read")
    args = parser.parse_args()

    print(fasterDeltat(args.files,
                       args.label, args.reflabel,
                       args.nbins, args.tmin, args.tmax))
