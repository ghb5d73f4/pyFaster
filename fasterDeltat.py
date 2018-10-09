'''
Compute an histogram of delta_t between a reference channel and a label

Usage:
 $ fasterDeltat.py --label=% --reflabel=% [--tmin=%] [--tmax=%] [--nbins=% [--nmax=%] ]file.fast 
'''

import faster
from pyhisto import Histogram as histo
import parse_args
import sys,os

if __name__=="__main__":
    try:
        args = {'label':0, 'reflabel':0,
                'nmax':1000,
                'tmin':-25000, 'tmax':65000, 'nbins':2000,
                }
        args.update(parse_args.parse_args())
        
        assert(args['label']>0)
        assert(len(args['free_params'])>=1)
        assert(args['reflabel']>0)

        h1 = histo(args['nbins'],
                   args['tmin'], args['tmax'])

        previous_ref_time = 0
                
        for f in args['free_params']:
            assert(os.path.exists(f))
            assert(os.path.isfile(f))
        
            for evt in faster.File_reader(f, args['nmax']):
                if evt.label==args['reflabel']:
                    previous_ref_time=evt.time
                elif evt.label==args['label']:
                    h1.fast_fill(evt.time-previous_ref_time)
                elif evt.type=='group':
                    for subevt in evt.data:
                        if subevt.label==args['reflabel']:
                            previous_ref_time=subevt.time
                        elif subevt.label==args['label']:
                            h1.fast_fill(subevt.time-previous_ref_time)
                
            #end for evt
        #end for f
        print(h1)                
        
    except:
        print(sys.exc_info())
        print(__doc__)
