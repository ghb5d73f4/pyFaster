import faster
from pyhisto import Histogram as histo

import struct

f = faster.File_reader("data/test_0001.fast", 500)

for evt in f:
    if evt.type=='group':
        for subevt in evt.data:
            #print(subevt.label)
            if subevt.type=='adc_event':
                z="".join(( format(x, "08b") for x in subevt.rawdata))[::-1]
                print(format(len(evt.data), "02"),
                      format(subevt.label, "02"),
                        z[:32], z[32:]
                    )
            pass
        pass
    #print("-")
