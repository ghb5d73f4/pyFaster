from pyhisto import Histogram as histo


import faster

filepath="data/test_0001.fast"

f = faster.File_reader(filepath, 500)


for evt in f:
    print(evt)

