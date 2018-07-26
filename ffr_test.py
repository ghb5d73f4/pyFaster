import faster

from pyhisto import Histogram as histo

f = faster.File_reader("data/test_0001.fast", 120)

for evt in f:
    if evt.type=='group':
        for subevt in evt.data:
            if subevt.type=='adc_event':
                print(subevt.rawdata)
