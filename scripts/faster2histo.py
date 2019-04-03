'''
Select a label and outputs ADC energy 

Usage:
 $ faster2histo.py --label=% file.fast 
'''

import sys,os

import argparse

import faster
#from pyhisto import Histogram as histo
from pyhisto import LazyHistogram as histo
from pyhisto import GhostHistogram as ghisto
#import parse_args


def faster2histo(files,
                 label=0,
                 nmax=faster.const.max_number_of_events_in_file,
                 nbins=1000, xmin=0, xmax=faster.const.max_adc_amplitude):
    '''Read a series of files and return and histogram'''
    try:        
        houtput = histo(nbins, xmin, xmax)
              
        for f in files:
            for evt in faster.FileReader(f, nmax):
                if evt.type_alias==10:
                    for subevt in evt.data['events']:
                        if subevt.label==label:
                            houtput.fast_fill(subevt.data['value'])
                elif evt.label==label:
                    houtput.fast_fill(evt.data['value'])
            #end for evt
        #end for f
        return houtput                
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)   
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
    parser.add_argument('--nbins', type=int, 
                        default=1000, nargs='?', 
                        help='number of bins in histogram')
    parser.add_argument('--xmin', type=float, 
                        default=0.0, nargs='?', 
                        help='minimum value in histogram')
    parser.add_argument('--xmax', type=float, 
                        default=faster.const.max_adc_amplitude,
                        nargs='?', 
                        help='maximum value in histogram')
    parser.add_argument('files', type=str,
                        nargs='*', help="Faster files to read")
    args = parser.parse_args()

    print(faster2histo(args.files, args.label,
                       args.nmax,
                       args.nbins, args.xmin, args.xmax))
