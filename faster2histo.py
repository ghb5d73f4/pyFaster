'''
Select a label and outputs ADC energy 

Usage:
 $ faster2histo.py --label=% file.fast 
'''

import faster
#from pyhisto import Histogram as histo
from pyhisto import LazyHistogram as histo
from pyhisto import GhostHistogram as ghisto
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

        outputs = {args['label']: histo(args['nbins'],
                                        args['xmin'], args['xmax']),
                   }
        hnull = ghisto()

              
        for f in args['free_params']:
            assert(os.path.exists(f))
            assert(os.path.isfile(f))
        
            for evt in faster.File_reader(f, args['nmax']):
                if evt.type_alias==10:
                    for subevt in evt.data['events']:
                        if subevt.label==args['label']:
                            outputs[subevt.label].fast_fill(subevt.data['value'])
                elif evt.label==args['label']:
                    outputs[evt.label].fast_fill(evt.data['value'])
            #end for evt
        #end for f
        print(outputs[args['label']])                
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)   
        print(__doc__)
