import faster
from pyhisto import Histogram as histo



filepath="data/test_0001.fast"
#filepath="../../../Downloads/FASTER/IPHC/ACQ/DATA/RUN_1_0001.fast"
#filepath="/work/ghenning/sandbox/fasterdata/RUN_1_0001.fast"

f = faster.File_reader(filepath, 500)


i = 0
for evt in f:
    print(evt)
    #    if evt.type=='group':
#        for subevt in evt.data:
#            if subevt.label==15:
#                h1.fast_fill(subevt.data['value']*0.1026+8.7)
#            print("\n      0x{0:08X} 0b{0:032b}".format(struct.unpack("<LL",subevt.rawdata)[1]))
#            print("     ",subevt)
#    i+=1

#print(h1)

