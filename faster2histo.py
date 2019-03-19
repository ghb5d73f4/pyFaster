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
                        required=True,
                        nargs='*', help="Faster files to read")
    args = parser.parse_args()
    try:        
        assert(args.label>0)

        houtput = histo(args.nbins, args.xmin, args.xmax)

              
        for f in args.files:
            assert(os.path.exists(f))
            assert(os.path.isfile(f))
        
            for evt in faster.File_reader(f, args.nmax):
                if evt.type_alias==10:
                    for subevt in evt.data['events']:
                        if subevt.label==args.label:
                            houtput.fast_fill(subevt.data['value'])
                elif evt.label==args.label:
                    houtput.fast_fill(evt.data['value'])
            #end for evt
        #end for f
        print(houtput)                
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)   
        print(__doc__)
