'''
Select a label and outputs ADC energy 

Usage:
 $ faster2histo.py --label=% file.fast 
'''

import faster
from pyhisto import Histogram as histo
import parse_args
import sys,os

if __name__=="__main__":
    try:
        args = {'label':0,
                'nbins':1000,
                'xmin':0, 'xmax':faster.const.max_adc_amplitude,
                'nmax':faster.const.max_number_of_events_in_file}
        args.update(parse_args.parse_args())
        
        assert(args['label']>0)
        assert(len(args['free_params'])>=1)


        h1 = histo(args['nbins'],
                   args['xmin'], args['xmax'])
                
        for f in args['free_params']:
            assert(os.path.exists(f))
            assert(os.path.isfile(f))
        
            for evt in faster.File_reader(f, args['nmax']):
                if evt.label==args['label']:
                    h1.fast_fill(evt.data['value'])
                elif evt.type=='group':
                    for subevt in evt.data:
                        if subevt.label==args['label']:
                            h1.fast_fill(subevt.data['value'])
                
            #end for evt
        #end for f
        print(h1)                
        
    except:
        print(sys.exc_info())
        print(__doc__)
